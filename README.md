# LLM API Service

Production-ready API service cho Large Language Models thông qua Ollama.

---

## 🚀 Quick Start

### 1. Setup Ollama & Model

```bash
# Check GPU và pull model
python setup_ollama_model.py

# Hoặc manual
ollama serve
ollama pull qwen3.5:4b
```

### 2. Install & Run

**Option A: Standalone (Single File)**
```bash
pip install -r requirements-minimal.txt
python llm_api_standalone.py
```

**Option B: Modular (Full Structure)**
```bash
cd LLM-Model
pip install -e ".[api]"
python -m api.main
```

### 3. Test API

```bash
curl http://localhost:8000/health/ready
curl -X POST http://localhost:8000/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is AI?", "max_tokens": 100}'
```

---

## 📁 Structure

```
.
├── setup_ollama_model.py         # Setup script (GPU check + model pull)
│
├── llm_api_standalone.py         # Single-file API (quick deploy)
│
├── LLM-Model/                    # Modular structure (production)
│   ├── llm/                      # Core service
│   ├── api/                      # FastAPI endpoints
│   ├── tests/                    # Test suite
│   └── pyproject.toml
│
├── pyproject.toml                # Standalone config
├── requirements.txt              # Dependencies
└── requirements-*.txt            # Specific use cases
```

---

## 📦 Installation

### Using pyproject.toml (Recommended)

```bash
# Standalone
pip install -e ".[api]"

# Modular
cd LLM-Model
pip install -e ".[api]"    # API only
pip install -e ".[dev]"    # Development
pip install -e ".[test]"   # Testing
```

### Using requirements.txt

```bash
# Minimal (standalone only)
pip install -r requirements-minimal.txt

# Full (all features)
pip install -r requirements.txt

# Development
pip install -r requirements-dev.txt

# Production
pip install -r requirements-production.txt
```

---

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health/live` | GET | Liveness probe |
| `/health/ready` | GET | Readiness probe |
| `/v1/generate` | POST | Text generation |
| `/v1/chat` | POST | Chat conversation |

**Docs:** http://localhost:8000/docs

---

## ⚙️ Configuration

Environment variables (`.env`):

```bash
MODEL_NAME=qwen3.5:4b
OLLAMA_URL=http://localhost:11434
API_PORT=8000
DEFAULT_TEMPERATURE=0.7
ENABLE_METRICS=true
LOG_LEVEL=INFO
```

---

## 🐳 Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY llm_api_standalone.py .
COPY requirements-minimal.txt .
RUN pip install -r requirements-minimal.txt
CMD ["python", "llm_api_standalone.py"]
```

```bash
docker build -t llm-api .
docker run -p 8000:8000 llm-api
```

---

## 🧪 Testing

```bash
cd LLM-Model
pip install -e ".[test]"
pytest
```

---

## 📊 Features

✅ **Stateless design** - No global state  
✅ **Error handling** - Ollama unavailable/timeout/model not found  
✅ **Metrics** - TTFT, TBT, tokens/s (optional)  
✅ **Logging** - Request ID, latency tracking  
✅ **Type safe** - Pydantic validation  
✅ **Production ready** - Timeout, concurrency safe  

---

## 💡 Use Cases

**Development:**
```bash
cd LLM-Model
pip install -e ".[dev]"
python -m api.main
```

**Quick Demo:**
```bash
pip install -r requirements-minimal.txt
python llm_api_standalone.py
```

**Production:**
```bash
pip install -r requirements-production.txt
gunicorn api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

---

## 🔧 Tools

### setup_ollama_model.py

Check GPU và pull Ollama model.

```bash
# Default model (qwen3.5:4b)
python setup_ollama_model.py

# Specific model
python setup_ollama_model.py --model qwen3.5:7b

# List only
python setup_ollama_model.py --list-only
```

### llm_api_standalone.py

Single-file API với tất cả features. Không cần install LLM-Model package.

### LLM-Model/

Modular structure với proper testing, documentation, và separation of concerns.

---

## 🎯 Quick Reference

**Setup:**
```bash
python setup_ollama_model.py
```

**Run Standalone:**
```bash
pip install -r requirements-minimal.txt
python llm_api_standalone.py
```

**Run Modular:**
```bash
cd LLM-Model
pip install -e ".[api]"
python -m api.main
```

**Test:**
```bash
curl http://localhost:8000/health/ready
```

---

## 📝 Requirements

- Python 3.9+
- Ollama installed and running
- Model downloaded (qwen3.5:4b)

---

## 🔗 Links

- **Ollama:** https://ollama.com
- **Qwen Models:** https://ollama.com/library/qwen3.5
- **API Docs:** http://localhost:8000/docs (after start)

---

## 📄 License

MIT

---

**🎉 Ready to use! Choose standalone for quick deploy or modular for production.**
