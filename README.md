# LLM API Service

Production-ready API service cho Large Language Models thông qua Ollama.

---

## 📤 Đẩy Lên GitHub & Chạy API

### Bước 1: Tạo repo trên GitHub

1. Vào https://github.com/new
2. Đặt tên repo (ví dụ: `llm-api-service`)
3. Để **Private** hoặc **Public** tùy ý
4. **Không** tick "Add README" (đã có sẵn)
5. Bấm **Create repository**

### Bước 2: Push code lên GitHub

Mở terminal tại thư mục dự án (`d:\Downloads`):

```bash
git init
git add .
git commit -m "first commit: LLM API with qwen3.5:4b"
git branch -M main
git remote add origin https://github.com/<username>/<repo-name>.git
git push -u origin main
```

> ⚠️ File `.env` đã được thêm vào `.gitignore` — **không bao giờ push file này lên GitHub**.

### Bước 3: Clone và chạy trên máy khác

```bash
# Clone repo
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>

# Tạo virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Activate (Linux/Mac)
# source .venv/bin/activate

# Cài dependencies
pip install -r LLM-Model/requirements.txt
# hoặc dùng standalone:
# pip install fastapi uvicorn ollama pydantic pydantic-settings python-dotenv
```

### Bước 4: Setup Ollama & model

```bash
# Cài Ollama nếu chưa có: https://ollama.com/download
# Khởi động Ollama (terminal riêng)
ollama serve

# Kéo model (terminal khác)
python setup_ollama_model.py
# hoặc thủ công:
# ollama pull qwen3.5:4b
```

### Bước 5: Tạo file .env

```bash
# Copy từ template
copy LLM-Model\.env.example .env
# Linux/Mac: cp LLM-Model/.env.example .env
```

Nội dung mặc định đã đúng, không cần sửa gì thêm:
```
MODEL_NAME=qwen3.5:4b
OLLAMA_URL=http://localhost:11434
API_PORT=8000
```

### Bước 6: Chạy API

**Option A — Standalone (1 file, đơn giản nhất):**
```bash
python llm_api_standalone.py
```

**Option B — Modular (production):**
```bash
cd LLM-Model
pip install -e ".[api]"
python -m api.main
```

### Bước 7: Test API đang chạy

```bash
# Health check
curl http://localhost:8000/health/ready

# Generate text
curl -X POST http://localhost:8000/v1/generate \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"What is AI?\", \"max_tokens\": 100}"

# Chat
curl -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -d "{\"messages\": [{\"role\": \"user\", \"content\": \"Hello!\"}]}"
```

Hoặc mở trình duyệt: **http://localhost:8000/docs** (Swagger UI)

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
python setup_ollama_model.py --model qwen3.5:4b

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
