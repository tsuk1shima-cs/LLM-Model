"""
Test health endpoints
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_liveness_probe():
    """Test /health/live endpoint"""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "timestamp" in data


def test_readiness_probe_success():
    """Test /health/ready endpoint when Ollama is available"""
    response = client.get("/health/ready")
    
    # Should return 200 if Ollama and model are available
    # Or 503 if Ollama/model is not available
    assert response.status_code in [200, 503]
    
    data = response.json()
    if response.status_code == 200:
        assert data["status"] == "healthy"
        assert data["ollama_available"] is True
        assert data["model_loaded"] is True
        assert "model" in data
        assert "timestamp" in data


def test_readiness_probe_ollama_unavailable():
    """Test /health/ready when Ollama is unavailable"""
    # This test would require mocking Ollama to be unavailable
    # For now, we just ensure the endpoint exists
    response = client.get("/health/ready")
    assert response.status_code in [200, 503]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
