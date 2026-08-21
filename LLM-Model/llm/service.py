"""
LLM Service - Core stateless service for Ollama interactions
Handles generation, chat, health checks, and optional metrics tracking
"""

import time
import logging
from typing import Optional, Dict, Any, List, Iterator
from datetime import datetime
import statistics

import ollama

from llm.config import Settings
from llm.errors import (
    OllamaUnavailableError,
    ModelNotFoundError,
    GenerationTimeoutError,
)
from llm.schemas import MetricsData


logger = logging.getLogger(__name__)


class LLMService:
    """
    Stateless LLM service for Ollama interactions.
    Each request is independent, no global state maintained.
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize LLM service with configuration.
        
        Args:
            settings: Configuration settings
        """
        self.settings = settings
        self.model_name = settings.model_name
        self.timeout = settings.ollama_timeout
        
        # Configure Ollama client
        if settings.ollama_url != "http://localhost:11434":
            ollama.Client(host=settings.ollama_url)
        
        logger.info(f"LLMService initialized with model={self.model_name}, timeout={self.timeout}s")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Check Ollama availability and model status.
        
        Returns:
            Dict with status information
            
        Raises:
            OllamaUnavailableError: If Ollama is not reachable
        """
        ollama_available = False
        model_loaded = False
        error_message = None
        
        try:
            # Try to get model info to verify connection and model availability
            info = ollama.show(self.model_name)
            ollama_available = True
            model_loaded = True
            logger.info(f"Health check passed: model {self.model_name} available")
            
        except ollama.ResponseError as e:
            if e.status_code == 404:
                # Ollama is reachable but model not found
                ollama_available = True
                model_loaded = False
                error_message = f"Model {self.model_name} not found"
                logger.warning(error_message)
            else:
                # Other Ollama errors
                error_message = f"Ollama error: {str(e)}"
                logger.error(error_message)
                
        except Exception as e:
            # Connection failed
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
        """
        Generate text from prompt (stateless).
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (uses default if None)
            top_p: Nucleus sampling parameter (uses default if None)
            max_tokens: Maximum tokens to generate (uses default if None)
            track_metrics: Whether to track detailed metrics (TTFT, TBT)
            request_id: Optional request ID for logging
            
        Returns:
            Dict containing:
                - response: Generated text
                - metrics: Performance metrics (if track_metrics=True)
                
        Raises:
            OllamaUnavailableError: If Ollama is not reachable
            ModelNotFoundError: If model is not found
            GenerationTimeoutError: If generation exceeds timeout
        """
        start_time = time.time()
        log_prefix = f"[{request_id}] " if request_id else ""
        
        # Use defaults if not specified
        temperature = temperature if temperature is not None else self.settings.default_temperature
        top_p = top_p if top_p is not None else self.settings.default_top_p
        max_tokens = max_tokens if max_tokens is not None else self.settings.default_max_tokens
        
        if self.settings.log_prompts:
            logger.info(f"{log_prefix}Generate: prompt='{prompt[:50]}...' temp={temperature}")
        else:
            logger.info(f"{log_prefix}Generate: prompt_len={len(prompt)} temp={temperature}")
        
        try:
            if track_metrics and self.settings.enable_metrics:
                # Track detailed metrics with streaming
                response_text, metrics = self._generate_with_metrics(
                    prompt, temperature, top_p, max_tokens
                )
            else:
                # Simple generation without metrics
                response_text = self._generate_simple(
                    prompt, temperature, top_p, max_tokens, start_time
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
        """
        Chat conversation (stateless - messages provided per request).
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            max_tokens: Maximum tokens to generate
            request_id: Optional request ID for logging
            
        Returns:
            Dict containing:
                - message: Assistant's response message dict
                
        Raises:
            OllamaUnavailableError: If Ollama is not reachable
            ModelNotFoundError: If model is not found
            GenerationTimeoutError: If chat exceeds timeout
        """
        start_time = time.time()
        log_prefix = f"[{request_id}] " if request_id else ""
        
        # Use defaults if not specified
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
        start_time: float,
    ) -> str:
        """Generate without metrics tracking."""
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
        """Generate with detailed TTFT and TBT metrics tracking."""
        start_time = time.time()
        first_token_time = None
        token_times = []
        last_token_time = start_time
        
        full_response = ""
        token_count = 0
        
        # Stream to capture timing per token
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
            
            # Capture TTFT (time to first token)
            if first_token_time is None:
                first_token_time = current_time - start_time
            
            # Capture TBT (time between tokens)
            if token_count > 0:
                tbt = current_time - last_token_time
                token_times.append(tbt)
            
            full_response += chunk['response']
            token_count += 1
            last_token_time = current_time
        
        # Calculate metrics
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
