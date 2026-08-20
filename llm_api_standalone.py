#!/usr/bin/env python3
"""
LLM API Service - Standalone Version
All-in-one file cho production deployment với Ollama

Usage:
    python llm_api_standalone.py

Environment Variables:
    MODEL_NAME=qwen3.5:4b
    OLLAMA_URL=http://localhost:11434
    API_PORT=8000
    OLLAMA_TIMEOUT=120

Endpoints:
    GET  /health/live      - Liveness probe
    GET  /health/ready     - Readiness probe  
    POST /v1/generate      - Text generation
    POST /v1/chat          - Chat conversation
"""

import os
import time
import uuid
import logging
import statistics
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any, List

# External dependencies
try:
    import ollama
    from fastapi import FastAPI, HTTPException, Request
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
    from pydantic_settings import BaseSettings
    import uvicorn
except ImportError as e:
    print("   Missing dependencies. Install with:")
    print("   pip install fastapi uvicorn ollama pydantic pydantic-settings")
    raise e


# ================================================================
# Configuration
# ================================================================

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Model configuration
    model_name: str = "qwen3.5:4b"
    
    # Ollama configuration
    ollama_url: str = "http://localhost:11434"
    ollama_timeout: int = 120
    
    # API configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Generation defaults
    default_temperature: float = 0.7
    default_top_p: float = 0.9
    default_max_tokens: int = 200
    
    # Logging
    log_level: str = "INFO"
    log_request_id: bool = True
    log_prompts: bool = False
    
    # Metrics
    enable_metrics: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()


# ================================================================
# Custom Exceptions
# ================================================================

class LLMError(Exception):
    """Base exception for all LLM service errors"""
    pass


class OllamaUnavailableError(LLMError):
    """Raised when Ollama server is not reachable"""
    def __init__(self, url: str, original_error: Exception = None):
        self.url = url
        self.original_error = original_error
        message = f"Ollama server unavailable at {url}"
        if original_error:
            message += f": {str(original_error)}"
        super().__init__(message)


class ModelNotFoundError(LLMError):
    """Raised when requested model is not available in Ollama"""
    def __init__(self, model_name: str):
        self.model_name = model_name
        super().__init__(f"Model '{model_name}' not found. Please run: ollama pull {model_name}")


class GenerationTimeoutError(LLMError):
    """Raised when generation exceeds timeout"""
    def __init__(self, timeout: int):
        self.timeout = timeout
        super().__init__(f"Generation exceeded timeout of {timeout} seconds")


# ================================================================
# Pydantic Schemas
# ================================================================

class Message(BaseModel):
    """Chat message model"""
    role: str = Field(..., description="Message role: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="Message content", min_length=1)


class GenerateRequest(BaseModel):
    """Request model for text generation"""
    prompt: str = Field(..., description="The prompt text", min_length=1)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=4096)


class GenerateResponse(BaseModel):
    """Response model for text generation"""
    response: str
    model: str
    metrics: Optional[Dict] = None
    timestamp: str


class ChatRequest(BaseModel):
    """Request model for chat conversation"""
    messages: List[Message] = Field(..., min_items=1)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=4096)


class ChatResponse(BaseModel):
    """Response model for chat conversation"""
    message: Message
    model: str
    timestamp: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model: str
    ollama_available: bool
    model_loaded: bool
    timestamp: str


# ================================================================
# LLM Service (Stateless)
# ================================================================

class LLMService:
    """
    Stateless LLM service for Ollama interactions.
    Each request is independent, no global state maintained.
    """
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.model_name = settings.model_name
        self.timeout = settings.ollama_timeout
        
        if settings.ollama_url != "http://localhost:11434":
            ollama.Client(host=settings.ollama_url)
        
        logger.info(f"LLMService initialized: model={self.model_name}, timeout={self.timeout}s")
    
    def health_check(self) -> Dict[str, Any]:
        """Check Ollama availability and model status"""
        ollama_available = False
        model_loaded = False
        error_message = None
        
        try:
            info = ollama.show(self.model_name)
            ollama_available = True
            model_loaded = True
            logger.info(f"Health check passed: model {self.model_name} available")
            
        except ollama.ResponseError as e:
            if e.status_code == 404:
                ollama_available = True
                model_loaded = False
                error_message = f"Model {self.model_name} not found"
                logger.warning(error_message)
            else:
                error_message = f"Ollama error: {str(e)}"
                logger.error(error_message)
                
        except Exception as e:
            error_message = f"Ollama unavailable: {str(e)}"
            logger.error(error_message)
        
        return {
            "ollama_available": ollama_available,
            "model_loaded": model_loaded,
            "model_name": self.model_name,
            "error": error_message,
        }
    
    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        track_metrics: bool = False,
        request_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate text from prompt (stateless)"""
        start_time = time.time()
        log_prefix = f"[{request_id}] " if request_id else ""
        
        temperature = temperature if temperature is not None else self.settings.default_temperature
        top_p = top_p if top_p is not None else self.settings.default_top_p
        max_tokens = max_tokens if max_tokens is not None else self.settings.default_max_tokens
        
        if self.settings.log_prompts:
            logger.info(f"{log_prefix}Generate: prompt='{prompt[:50]}...' temp={temperature}")
        else:
            logger.info(f"{log_prefix}Generate: prompt_len={len(prompt)} temp={temperature}")
        
        try:
            if track_metrics and self.settings.enable_metrics:
                response_text, metrics = self._generate_with_metrics(
                    prompt, temperature, top_p, max_tokens
                )
            else:
                response_text = self._generate_simple(
                    prompt, temperature, top_p, max_tokens
                )
                metrics = None
            
            elapsed = time.time() - start_time
            logger.info(f"{log_prefix}Generate completed in {elapsed:.3f}s")
            
            return {
                "response": response_text,
                "metrics": metrics,
            }
            
        except ollama.ResponseError as e:
            if e.status_code == 404:
                logger.error(f"{log_prefix}Model not found: {self.model_name}")
                raise ModelNotFoundError(self.model_name)
            else:
                logger.error(f"{log_prefix}Ollama error: {e}")
                raise OllamaUnavailableError(self.settings.ollama_url, e)
                
        except Exception as e:
            logger.error(f"{log_prefix}Generation failed: {e}")
            raise OllamaUnavailableError(self.settings.ollama_url, e)
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        request_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Chat conversation (stateless - messages provided per request)"""
        start_time = time.time()
        log_prefix = f"[{request_id}] " if request_id else ""
        
        temperature = temperature if temperature is not None else self.settings.default_temperature
        top_p = top_p if top_p is not None else self.settings.default_top_p
        max_tokens = max_tokens if max_tokens is not None else self.settings.default_max_tokens
        
        logger.info(f"{log_prefix}Chat: {len(messages)} messages, temp={temperature}")
        
        try:
            response = ollama.chat(
                model=self.model_name,
                messages=messages,
                options={
                    'temperature': temperature,
                    'top_p': top_p,
                    'num_predict': max_tokens,
                }
            )
            
            elapsed = time.time() - start_time
            logger.info(f"{log_prefix}Chat completed in {elapsed:.3f}s")
            
            return {
                "message": response['message'],
            }
            
        except ollama.ResponseError as e:
            if e.status_code == 404:
                logger.error(f"{log_prefix}Model not found: {self.model_name}")
                raise ModelNotFoundError(self.model_name)
            else:
                logger.error(f"{log_prefix}Ollama error: {e}")
                raise OllamaUnavailableError(self.settings.ollama_url, e)
                
        except Exception as e:
            logger.error(f"{log_prefix}Chat failed: {e}")
            raise OllamaUnavailableError(self.settings.ollama_url, e)
    
    def _generate_simple(
        self,
        prompt: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
    ) -> str:
        """Generate without metrics tracking"""
        response = ollama.generate(
            model=self.model_name,
            prompt=prompt,
            options={
                'temperature': temperature,
                'top_p': top_p,
                'num_predict': max_tokens,
            }
        )
        return response['response']
    
    def _generate_with_metrics(
        self,
        prompt: str,
        temperature: float,
        top_p: float,
        max_tokens: int,
    ) -> tuple[str, Dict[str, Any]]:
        """Generate with detailed TTFT and TBT metrics tracking"""
        start_time = time.time()
        first_token_time = None
        token_times = []
        last_token_time = start_time
        
        full_response = ""
        token_count = 0
        
        for chunk in ollama.generate(
            model=self.model_name,
            prompt=prompt,
            stream=True,
            options={
                'temperature': temperature,
                'top_p': top_p,
                'num_predict': max_tokens,
            }
        ):
            current_time = time.time()
            
            if first_token_time is None:
                first_token_time = current_time - start_time
            
            if token_count > 0:
                tbt = current_time - last_token_time
                token_times.append(tbt)
            
            full_response += chunk['response']
            token_count += 1
            last_token_time = current_time
        
        total_time = time.time() - start_time
        avg_tbt = statistics.mean(token_times) if token_times else 0
        tokens_per_second = token_count / total_time if total_time > 0 else 0
        
        metrics = {
            "ttft_ms": round(first_token_time * 1000, 2) if first_token_time else None,
            "avg_tbt_ms": round(avg_tbt * 1000, 2) if avg_tbt > 0 else None,
            "total_latency_ms": round(total_time * 1000, 2),
            "tokens_per_second": round(tokens_per_second, 2),
            "output_tokens": token_count,
        }
        
        logger.debug(f"Metrics: TTFT={metrics['ttft_ms']}ms, TPS={metrics['tokens_per_second']}")
        
        return full_response, metrics


# ================================================================
# FastAPI Application
# ================================================================

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Global service instance
llm_service: LLMService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle"""
    global llm_service
    
    # Startup
    logger.info("="*70)
    logger.info("   Starting LLM API Service")
    logger.info("="*70)
    logger.info(f"Model: {settings.model_name}")
    logger.info(f"Ollama URL: {settings.ollama_url}")
    logger.info(f"Timeout: {settings.ollama_timeout}s")
    logger.info(f"API: http://{settings.api_host}:{settings.api_port}")
    logger.info("="*70)
    
    llm_service = LLMService(settings)
    
    try:
        health = llm_service.health_check()
        if health["ollama_available"] and health["model_loaded"]:
            logger.info(f"✅ Model {settings.model_name} ready")
        elif health["ollama_available"]:
            logger.warning(f"  Ollama available but model not loaded")
        else:
            logger.error(f" Ollama unavailable: {health.get('error')}")
    except Exception as e:
        logger.error(f" Health check failed: {e}")
    
    yield
    
    logger.info("Shutting down LLM API Service...")


# Initialize FastAPI
app = FastAPI(
    title="LLM API Service",
    description="Production-ready API for Qwen LLM via Ollama",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware for request tracking
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID to each request"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = datetime.now()
    response = await call_next(request)
    elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
    
    response.headers["X-Request-ID"] = request_id
    
    if settings.log_request_id:
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"completed in {elapsed_ms:.2f}ms - status={response.status_code}"
        )
    
    return response


# ================================================================
# API Endpoints
# ================================================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "LLM API Service",
        "version": "1.0.0",
        "model": settings.model_name,
        "endpoints": {
            "docs": "/docs",
            "health_live": "/health/live",
            "health_ready": "/health/ready",
            "generate": "/v1/generate",
            "chat": "/v1/chat",
        },
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health/live", tags=["Health"])
async def liveness():
    """Liveness probe - checks if service is running"""
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health/ready", response_model=HealthResponse, tags=["Health"])
async def readiness():
    """Readiness probe - checks if service is ready to handle requests"""
    health = llm_service.health_check()
    
    if not health["ollama_available"]:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama unavailable: {health.get('error')}"
        )
    
    if not health["model_loaded"]:
        raise HTTPException(
            status_code=503,
            detail=f"Model {llm_service.model_name} not loaded"
        )
    
    return HealthResponse(
        status="healthy",
        model=llm_service.model_name,
        ollama_available=True,
        model_loaded=True,
        timestamp=datetime.now().isoformat(),
    )


@app.post("/v1/generate", response_model=GenerateResponse, tags=["Generation"])
async def generate_text(request: GenerateRequest, req: Request):
    """Generate text from a prompt"""
    request_id = req.state.request_id
    
    try:
        result = llm_service.generate(
            prompt=request.prompt,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
            track_metrics=settings.enable_metrics,
            request_id=request_id,
        )
        
        return GenerateResponse(
            response=result["response"],
            model=llm_service.model_name,
            metrics=result.get("metrics"),
            timestamp=datetime.now().isoformat(),
        )
        
    except ModelNotFoundError as e:
        logger.error(f"[{request_id}] Model not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
        
    except OllamaUnavailableError as e:
        logger.error(f"[{request_id}] Ollama unavailable: {e}")
        raise HTTPException(status_code=503, detail=str(e))
        
    except GenerationTimeoutError as e:
        logger.error(f"[{request_id}] Generation timeout: {e}")
        raise HTTPException(status_code=504, detail=str(e))
        
    except Exception as e:
        logger.error(f"[{request_id}] Generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.post("/v1/chat", response_model=ChatResponse, tags=["Chat"])
async def chat_conversation(request: ChatRequest, req: Request):
    """Multi-turn chat conversation (stateless)"""
    request_id = req.state.request_id
    
    try:
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        result = llm_service.chat(
            messages=messages,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
            request_id=request_id,
        )
        
        assistant_message = Message(
            role=result["message"]["role"],
            content=result["message"]["content"],
        )
        
        return ChatResponse(
            message=assistant_message,
            model=llm_service.model_name,
            timestamp=datetime.now().isoformat(),
        )
        
    except ModelNotFoundError as e:
        logger.error(f"[{request_id}] Model not found: {e}")
        raise HTTPException(status_code=404, detail=str(e))
        
    except OllamaUnavailableError as e:
        logger.error(f"[{request_id}] Ollama unavailable: {e}")
        raise HTTPException(status_code=503, detail=str(e))
        
    except GenerationTimeoutError as e:
        logger.error(f"[{request_id}] Chat timeout: {e}")
        raise HTTPException(status_code=504, detail=str(e))
        
    except Exception as e:
        logger.error(f"[{request_id}] Chat failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")


# ================================================================
# Main Entry Point
# ================================================================

if __name__ == "__main__":
    print("="*70)
    print(" LLM API Service - Standalone Version")
    print("="*70)
    print(f"Model: {settings.model_name}")
    print(f"Ollama: {settings.ollama_url}")
    print(f"API: http://{settings.api_host}:{settings.api_port}")
    print(f"Docs: http://localhost:{settings.api_port}/docs")
    print("="*70)
    print()
    
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
    )
