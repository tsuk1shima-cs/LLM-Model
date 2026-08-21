"""
FastAPI Application for LLM Service
Provides REST API endpoints for text generation and chat
"""

import logging
import uuid
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from llm import (
    LLMService,
    Settings,
    GenerateRequest,
    GenerateResponse,
    ChatRequest,
    ChatResponse,
    OllamaUnavailableError,
    ModelNotFoundError,
    GenerationTimeoutError,
)
from llm.schemas import HealthResponse


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Global settings and service (initialized on startup)
settings = Settings()
llm_service: LLMService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifecycle"""
    global llm_service
    
    # Startup
    logger.info("="*70)
    logger.info("🚀 Starting LLM API Service")
    logger.info("="*70)
    logger.info(f"Model: {settings.model_name}")
    logger.info(f"Ollama URL: {settings.ollama_url}")
    logger.info(f"Timeout: {settings.ollama_timeout}s")
    logger.info(f"API: http://{settings.api_host}:{settings.api_port}")
    logger.info("="*70)
    
    # Initialize service
    llm_service = LLMService(settings)
    
    # Check health
    try:
        health = llm_service.health_check()
        if health["ollama_available"] and health["model_loaded"]:
            logger.info(f"✅ Model {settings.model_name} ready")
        elif health["ollama_available"]:
            logger.warning(f"⚠️  Ollama available but model not loaded")
        else:
            logger.error(f"❌ Ollama unavailable: {health.get('error')}")
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down LLM API Service...")


# Initialize FastAPI app
app = FastAPI(
    title="LLM API Service",
    description="Production-ready API for Qwen LLM via Ollama",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get service instance
def get_llm_service() -> LLMService:
    """Dependency injection for LLM service"""
    if llm_service is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return llm_service


# Middleware to add request ID
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID to each request"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    start_time = datetime.now()
    response = await call_next(request)
    elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
    
    # Add request ID to response headers
    response.headers["X-Request-ID"] = request_id
    
    # Log request with latency
    if settings.log_request_id:
        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"completed in {elapsed_ms:.2f}ms - status={response.status_code}"
        )
    
    return response


# ================================================================
# Health Endpoints
# ================================================================

@app.get("/health/live", tags=["Health"])
async def liveness():
    """
    Liveness probe - checks if service is running.
    Returns 200 if the API server is alive.
    """
    return {
        "status": "alive",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/health/ready", response_model=HealthResponse, tags=["Health"])
async def readiness(service: LLMService = Depends(get_llm_service)):
    """
    Readiness probe - checks if service is ready to handle requests.
    Verifies Ollama connection and model availability.
    """
    health = service.health_check()
    
    if not health["ollama_available"]:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama unavailable: {health.get('error')}"
        )
    
    if not health["model_loaded"]:
        raise HTTPException(
            status_code=503,
            detail=f"Model {service.model_name} not loaded"
        )
    
    return HealthResponse(
        status="healthy",
        model=service.model_name,
        ollama_available=True,
        model_loaded=True,
        timestamp=datetime.now().isoformat(),
    )


# ================================================================
# Generation Endpoints
# ================================================================

@app.post("/v1/generate", response_model=GenerateResponse, tags=["Generation"])
async def generate_text(
    request: GenerateRequest,
    req: Request,
    service: LLMService = Depends(get_llm_service),
):
    """
    Generate text from a prompt.
    
    Takes a text prompt and generates a continuation using the configured LLM.
    
    - **prompt**: The input text to continue (required)
    - **temperature**: Controls randomness (0.0 = deterministic, 2.0 = very random)
    - **top_p**: Nucleus sampling parameter (0.0 to 1.0)
    - **max_tokens**: Maximum number of tokens to generate
    """
    request_id = req.state.request_id
    
    try:
        result = service.generate(
            prompt=request.prompt,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
            track_metrics=settings.enable_metrics,
            request_id=request_id,
        )
        
        return GenerateResponse(
            response=result["response"],
            model=service.model_name,
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
async def chat_conversation(
    request: ChatRequest,
    req: Request,
    service: LLMService = Depends(get_llm_service),
):
    """
    Multi-turn chat conversation (stateless).
    
    Each request is independent - provide full conversation history in messages.
    
    - **messages**: List of message objects with role and content (required)
    - **temperature**: Controls randomness
    - **top_p**: Nucleus sampling parameter
    - **max_tokens**: Maximum tokens for the response
    
    Message roles:
    - **user**: User's message
    - **assistant**: Model's previous responses
    - **system**: System instruction (optional)
    """
    request_id = req.state.request_id
    
    try:
        # Convert Pydantic messages to dicts for service
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]
        
        result = service.chat(
            messages=messages,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
            request_id=request_id,
        )
        
        # Convert back to Pydantic Message
        from llm.schemas import Message
        assistant_message = Message(
            role=result["message"]["role"],
            content=result["message"]["content"],
        )
        
        return ChatResponse(
            message=assistant_message,
            model=service.model_name,
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
# Root Endpoint
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


# ================================================================
# Main Entry Point
# ================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
    )
