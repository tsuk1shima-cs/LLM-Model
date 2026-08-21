"""
Configuration management for LLM service
Loads from environment variables with sensible defaults
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Model configuration
    model_name: str = "qwen3.5:4b"
    
    # Ollama configuration
    ollama_url: str = "http://localhost:11434"
    ollama_timeout: int = 120  # seconds
    
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
    log_prompts: bool = False  # Don't log prompts by default for privacy
    
    # Metrics
    enable_metrics: bool = True
    metrics_export_path: str = "."
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
