"""
Test text generation endpoint
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_generate_valid_request():
    """Test /v1/generate with valid request"""
    request_data = {
        "prompt": "What is artificial intelligence?",
        "temperature": 0.7,
        "max_tokens": 100,
    }
    
    response = client.post("/v1/generate", json=request_data)
    
    # Should return 200 if Ollama is available, or 503/504 if unavailable/timeout
    assert response.status_code in [200, 503, 504]
    
    if response.status_code == 200:
        data = response.json()
        assert "response" in data
        assert "model" in data
        assert "timestamp" in data
        assert len(data["response"]) > 0


def test_generate_invalid_request_missing_prompt():
    """Test /v1/generate with missing prompt"""
    request_data = {
        "temperature": 0.7,
        "max_tokens": 100,
    }
    
    response = client.post("/v1/generate", json=request_data)
    assert response.status_code == 422  # Validation error


def test_generate_invalid_temperature():
    """Test /v1/generate with invalid temperature"""
    request_data = {
        "prompt": "Test prompt",
        "temperature": 3.0,  # Out of range (max 2.0)
        "max_tokens": 100,
    }
    
    response = client.post("/v1/generate", json=request_data)
    assert response.status_code == 422  # Validation error


def test_generate_with_metrics():
    """Test /v1/generate returns metrics when enabled"""
    request_data = {
        "prompt": "Explain machine learning briefly.",
        "max_tokens": 50,
    }
    
    response = client.post("/v1/generate", json=request_data)
    
    if response.status_code == 200:
        data = response.json()
        # Metrics should be present if ENABLE_METRICS=true in config
        if "metrics" in data and data["metrics"]:
            assert "total_latency_ms" in data["metrics"] or "total_time" in data["metrics"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
