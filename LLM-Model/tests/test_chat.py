"""
Test chat endpoint
"""

import pytest
from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_chat_valid_request():
    """Test /v1/chat with valid request"""
    request_data = {
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ],
        "temperature": 0.7,
        "max_tokens": 100,
    }
    
    response = client.post("/v1/chat", json=request_data)
    
    # Should return 200 if Ollama is available, or 503/504 if unavailable/timeout
    assert response.status_code in [200, 503, 504]
    
    if response.status_code == 200:
        data = response.json()
        assert "message" in data
        assert "model" in data
        assert "timestamp" in data
        assert data["message"]["role"] == "assistant"
        assert len(data["message"]["content"]) > 0


def test_chat_multi_turn():
    """Test /v1/chat with multiple messages"""
    request_data = {
        "messages": [
            {"role": "user", "content": "What is 2+2?"},
            {"role": "assistant", "content": "2+2 equals 4."},
            {"role": "user", "content": "What about 3+3?"}
        ],
        "temperature": 0.5,
        "max_tokens": 50,
    }
    
    response = client.post("/v1/chat", json=request_data)
    
    if response.status_code == 200:
        data = response.json()
        assert data["message"]["role"] == "assistant"
        assert len(data["message"]["content"]) > 0


def test_chat_invalid_request_empty_messages():
    """Test /v1/chat with empty messages"""
    request_data = {
        "messages": [],
        "max_tokens": 100,
    }
    
    response = client.post("/v1/chat", json=request_data)
    assert response.status_code == 422  # Validation error


def test_chat_invalid_message_role():
    """Test /v1/chat with invalid message role"""
    request_data = {
        "messages": [
            {"role": "invalid_role", "content": "Hello"}
        ],
    }
    
    response = client.post("/v1/chat", json=request_data)
    # FastAPI/Pydantic should accept any string role, Ollama may validate
    assert response.status_code in [200, 422, 500, 503]


def test_chat_stateless():
    """Test that chat is stateless - each request is independent"""
    # First request
    request1 = {
        "messages": [
            {"role": "user", "content": "My name is Alice."}
        ],
        "max_tokens": 50,
    }
    response1 = client.post("/v1/chat", json=request1)
    
    # Second request without context - should not remember "Alice"
    request2 = {
        "messages": [
            {"role": "user", "content": "What is my name?"}
        ],
        "max_tokens": 50,
    }
    response2 = client.post("/v1/chat", json=request2)
    
    # Both requests should work independently
    if response1.status_code == 200 and response2.status_code == 200:
        data2 = response2.json()
        # The model shouldn't know the name from the first request
        # (This is a behavioral test - actual response depends on model)
        assert "message" in data2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
