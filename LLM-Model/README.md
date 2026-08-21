# LLM-Model: Production-Ready LLM API Service

API Service cho Large Language Model thông qua Ollama. Thiết kế stateless, production-ready với đầy đủ error handling, timeout, metrics tracking.

## 🎯 Definition of Done

Sau khi hoàn thành các bước dưới đây, bạn có thể test các endpoint:

```bash
# 1. Clone repository
git clone <repository-url>
cd LLM-Model

# 2. Tạo virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

# 3. Install dependencies
pip install -e ".[api]"

# 4. Setup Ollama và model
ollama serve                    # Terminal 1
ollama pull qwen3.5:4b         # Terminal 2

# 5. Start API server
python -m api.main

# 6. Test endpoints
```

Sau đó các endpoint phải PASS:

| Endpoint | Method | Mô tả | Expected |
|----------|--------|-------|----------|
| `/health/live` | GET | Liveness probe | ✅ PASS (200) |
| `/health/ready` | GET | Readiness probe | ✅ PASS (200) |
| `/v1/generate` | POST | Text generation | ✅ PASS (200) |
| `/v1/chat` | POST | Chat conversation | ✅ PASS (200) |

---

## 📁 Cấu Trúc Module

```
LLM-Model/
├── llm/                    # Core service module
│   ├── __init__.py         # Package exports
│   ├── service.py          # LLMService (stateless, no global messages)
│   ├── config.py           # Settings từ environment variables
│   ├── schemas.py          # Pydantic request/response models
│   └── errors.py           # Custom exceptions
│
├── api/                    # FastAPI application
│   ├── __init__.py
│   └── main.py             # API endpoints: health/live, health/ready, generate, chat
│
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── test_health.py      # Test health endpoints
│   ├── test_generate.py    # Test /v1/generate
│   └── test_chat.py        # Test /v1/chat
│
├── scripts/
│   └── setup_ollama.sh     # Script để setup Ollama + pull model
│
├── pyproject.toml          # Dependencies + install config
├── .env.example            # Environment variables template
└── README.md               # Tài liệu này
```

### ✅ Yêu Cầu Đã Hoàn Thành

- ✅ **Tách module rõ ràng**: service / api / schemas / config / errors
- ✅ **Runtime model check**: Ollama + model được kiểm tra trạng thái trong health/ready
- ✅ **API endpoints**: `/health/live`, `/health/ready`, `/v1/generate`, `/v1/chat`
- ✅ **Stateless**: Không dùng global messages; mỗi request độc lập
- ✅ **Pydantic schemas**: Validate request/response đầy đủ
- ✅ **Config từ env**: Model name, Ollama URL, port, temperature, max_tokens...
- ✅ **Error handling**: Ollama unavailable/model not found/timeout trả lỗi rõ ràng
- ✅ **Timeout**: Có timeout khi gọi Ollama
- ✅ **Concurrency safe**: Không có state chia sẻ giữa các request
- ✅ **Runtime metrics**: TTFT, total latency, tokens/s (optional)
- ✅ **Logging**: Request ID, latency, model; không dump prompt mặc định
- ✅ **Streaming ready**: Thiết kế sẵn sàng để thêm streaming sau
- ✅ **RAG contract**: LLM chỉ nhận messages/prompt đã build sẵn
- ✅ **Tests**: Health, generate, chat, invalid request, Ollama unavailable
- ✅ **pyproject.toml**: `pip install -e ".[api]"` để install

---

## 🚀 Hướng Dẫn Sử Dụng

### Bước 1: Clone và Setup Environment

```bash
git clone <repository-url>
cd LLM-Model

# Tạo virtual environment
python -m venv .venv

# Activate
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux/Mac

# Install package với API dependencies
pip install -e ".[api]"
```

### Bước 2: Setup Ollama

**Option 1: Manual**
```bash
# Start Ollama server
ollama serve

# Pull model (terminal khác)
ollama pull qwen3.5:4b

# Verify
ollama list
```

**Option 2: Dùng script**
```bash
bash scripts/setup_ollama.sh
```

### Bước 3: Configure Environment

```bash
# Copy template
cp .env.example .env

# Edit .env nếu cần
# MODEL_NAME=qwen3.5:4b
# OLLAMA_URL=http://localhost:11434
# API_PORT=8000
```

### Bước 4: Start API Server

```bash
python -m api.main
```

Output mong đợi:
```
======================================================================
🚀 Starting LLM API Service
======================================================================
Model: qwen3.5:4b
Ollama URL: http://localhost:11434
Timeout: 120s
API: http://0.0.0.0:8000
======================================================================
✅ Model qwen3.5:4b ready
```

### Bước 5: Test API

**Health Checks:**
```bash
# Liveness (server alive?)
curl http://localhost:8000/health/live

# Readiness (Ollama + model ready?)
curl http://localhost:8000/health/ready
```

**Generate Text:**
```bash
curl -X POST http://localhost:8000/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is artificial intelligence?",
    "temperature": 0.7,
    "max_tokens": 200
  }'
```

**Chat Conversation:**
```bash
curl -X POST http://localhost:8000/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "temperature": 0.7,
    "max_tokens": 200
  }'
```

**Interactive Docs:**
Mở trình duyệt: `http://localhost:8000/docs`

---

## 📡 API Endpoints

### Health Endpoints

#### `GET /health/live`
Liveness probe - kiểm tra API server có đang chạy không.

**Response 200:**
```json
{
  "status": "alive",
  "timestamp": "2026-08-20T22:30:00"
}
```

#### `GET /health/ready`
Readiness probe - kiểm tra Ollama connection và model availability.

**Response 200 (Ready):**
```json
{
  "status": "healthy",
  "model": "qwen3.5:4b",
  "ollama_available": true,
  "model_loaded": true,
  "timestamp": "2026-08-20T22:30:00"
}
```

**Response 503 (Not Ready):**
```json
{
  "detail": "Ollama unavailable: Connection refused"
}
```

### Generation Endpoints

#### `POST /v1/generate`
Generate text từ prompt.

**Request Body:**
```json
{
  "prompt": "What is artificial intelligence?",
  "temperature": 0.7,
  "top_p": 0.9,
  "max_tokens": 200
}
```

**Response 200:**
```json
{
  "response": "Artificial intelligence (AI) is...",
  "model": "qwen3.5:4b",
  "metrics": {
    "ttft_ms": 125.5,
    "avg_tbt_ms": 15.2,
    "total_latency_ms": 1850,
    "tokens_per_second": 45.3,
    "output_tokens": 87
  },
  "timestamp": "2026-08-20T22:30:00"
}
```

**Errors:**
- `404`: Model not found
- `503`: Ollama unavailable
- `504`: Generation timeout
- `422`: Invalid request parameters

#### `POST /v1/chat`
Multi-turn chat conversation (stateless).

**Request Body:**
```json
{
  "messages": [
    {"role": "user", "content": "What is 2+2?"},
    {"role": "assistant", "content": "2+2 equals 4."},
    {"role": "user", "content": "What about 3+3?"}
  ],
  "temperature": 0.7,
  "max_tokens": 200
}
```

**Response 200:**
```json
{
  "message": {
    "role": "assistant",
    "content": "3+3 equals 6."
  },
  "model": "qwen3.5:4b",
  "timestamp": "2026-08-20T22:30:00"
}
```

**Note:** Chat là **stateless** - phải gửi toàn bộ conversation history trong mỗi request.

---

## ⚙️ Configuration

Toàn bộ config qua **environment variables** (file `.env`):

| Variable | Default | Mô tả |
|----------|---------|-------|
| `MODEL_NAME` | `qwen3.5:4b` | Tên model trong Ollama |
| `OLLAMA_URL` | `http://localhost:11434` | URL của Ollama server |
| `OLLAMA_TIMEOUT` | `120` | Timeout (giây) cho Ollama requests |
| `API_HOST` | `0.0.0.0` | Host để bind API server |
| `API_PORT` | `8000` | Port của API server |
| `DEFAULT_TEMPERATURE` | `0.7` | Temperature mặc định (0.0-2.0) |
| `DEFAULT_TOP_P` | `0.9` | Top-P mặc định (0.0-1.0) |
| `DEFAULT_MAX_TOKENS` | `200` | Max tokens mặc định |
| `LOG_LEVEL` | `INFO` | Log level (DEBUG/INFO/WARNING/ERROR) |
| `LOG_REQUEST_ID` | `true` | Log request IDs |
| `LOG_PROMPTS` | `false` | Log prompts (privacy concern) |
| `ENABLE_METRICS` | `true` | Enable TTFT/TBT tracking |
| `METRICS_EXPORT_PATH` | `.` | Path để export metrics |

---

## 🔧 Error Handling

API trả về HTTP status codes rõ ràng:

| Status | Error | Mô tả |
|--------|-------|-------|
| `200` | Success | Request thành công |
| `404` | ModelNotFoundError | Model chưa được pull: `ollama pull <model>` |
| `422` | ValidationError | Request parameters không hợp lệ |
| `503` | OllamaUnavailableError | Ollama server không chạy hoặc unreachable |
| `504` | GenerationTimeoutError | Generation vượt quá timeout |
| `500` | InternalServerError | Lỗi không xác định |

Tất cả errors đều có `detail` message rõ ràng trong response body.

---

## 🧪 Testing

### Chạy Tests

```bash
# Install test dependencies
pip install -e ".[test]"

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_health.py -v

# Run with coverage
pytest tests/ --cov=llm --cov=api
```

### Test Coverage

- ✅ `test_health.py`: Liveness và readiness probes
- ✅ `test_generate.py`: Text generation, valid/invalid requests
- ✅ `test_chat.py`: Chat conversation, stateless behavior
- ✅ Error cases: Ollama unavailable, model not found, timeouts

---

## 📊 Metrics Tracking

Khi `ENABLE_METRICS=true`, API track các metrics sau:

- **TTFT** (Time To First Token): Latency đến token đầu tiên (ms)
- **TBT** (Time Between Tokens): Thời gian trung bình giữa các tokens (ms)
- **Total Latency**: Tổng thời gian generation (ms)
- **Throughput**: Tokens per second
- **Output Tokens**: Số tokens được generate

Metrics được trả về trong response khi available:

```json
{
  "response": "...",
  "metrics": {
    "ttft_ms": 125.5,
    "avg_tbt_ms": 15.2,
    "total_latency_ms": 1850,
    "tokens_per_second": 45.3,
    "output_tokens": 87
  }
}
```

---

## 🐳 Production Deployment

### Docker

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir ".[api]"

ENV OLLAMA_URL=http://ollama:11434
EXPOSE 8000

CMD ["python", "-m", "api.main"]
```

**Build & Run:**
```bash
docker build -t llm-api:latest .
docker run -p 8000:8000 -e OLLAMA_URL=http://host.docker.internal:11434 llm-api:latest
```

### Kubernetes

**Deployment với Health Probes:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: llm-api
        image: llm-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: OLLAMA_URL
          value: "http://ollama-service:11434"
        - name: MODEL_NAME
          value: "qwen3.5:4b"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 10
          failureThreshold: 3
```

### Load Balancing

API là stateless nên có thể scale horizontal dễ dàng:

```bash
# Multiple instances
python -m api.main &  # Instance 1 on port 8000
API_PORT=8001 python -m api.main &  # Instance 2 on port 8001
API_PORT=8002 python -m api.main &  # Instance 3 on port 8002

# Use nginx/HAProxy for load balancing
```

---

## 🔒 Security Best Practices

1. **Không log prompts mặc định**: Set `LOG_PROMPTS=false` để tránh leak sensitive data
2. **Request ID tracking**: Mỗi request có unique ID để audit
3. **Timeout protection**: Prevent long-running requests từ hang
4. **Input validation**: Pydantic validate tất cả inputs
5. **CORS configuration**: Configure `allow_origins` properly trong production
6. **Rate limiting**: Cân nhắc thêm rate limiting middleware
7. **Authentication**: Thêm API key hoặc OAuth nếu cần

---

## 📝 Logging

Logs có format rõ ràng với request tracking:

```
2026-08-20 22:30:15 - api.main - INFO - [a1b2c3d4-...] POST /v1/generate completed in 1850.25ms - status=200
2026-08-20 22:30:15 - llm.service - INFO - [a1b2c3d4-...] Generate completed in 1.845s
```

**Log levels:**
- `DEBUG`: Chi tiết metrics, parameters
- `INFO`: Request/response, latency
- `WARNING`: Model not loaded, retries
- `ERROR`: Ollama failures, timeouts

---

## 🚨 Troubleshooting

### Error: "Ollama unavailable"

```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### Error: "Model not found"

```bash
# Pull the model
ollama pull qwen3.5:4b

# Verify
ollama list
```

### Error: "Generation timeout"

- Tăng `OLLAMA_TIMEOUT` trong `.env`
- Check Ollama server resources (CPU/RAM)
- Giảm `max_tokens` trong request

### API không start

```bash
# Check port availability
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Try different port
API_PORT=8001 python -m api.main
```

---

## 🎯 RAG Integration Contract

LLM service này được thiết kế để integrate với RAG orchestrator:

**Contract:**
- LLM service **CHỈ nhận** messages hoặc prompt đã được build sẵn
- **KHÔNG** thực hiện retrieval, chunking, hoặc context building
- Orchestrator phải gửi full context trong `messages` (chat) hoặc `prompt` (generate)

**Example RAG Flow:**
```
User Query → RAG Orchestrator → [Retrieve + Build Context] → LLM API → Response
```

**LLM API chỉ làm:**
```json
{
  "messages": [
    {"role": "system", "content": "You are a helpful assistant. Use this context: [RAG context đã build sẵn]"},
    {"role": "user", "content": "User query"}
  ]
}
```

---

## 📚 Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

Bao gồm: API dependencies + test dependencies.

### Code Structure Guidelines

- **service.py**: Stateless, no global state, pure functions
- **config.py**: Environment-based configuration only
- **schemas.py**: Pydantic models, strict validation
- **errors.py**: Custom exceptions với clear messages
- **main.py**: FastAPI routes, middleware, dependency injection

### Adding New Endpoints

1. Define request/response schemas trong `schemas.py`
2. Add logic trong `service.py`
3. Create endpoint trong `api/main.py`
4. Write tests trong `tests/`
5. Update README

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 🙋 Support

**Issues:**
- Ollama không chạy: Check `ollama serve`
- Model không load: Run `ollama pull <model>`
- API errors: Check logs với `LOG_LEVEL=DEBUG`

**Documentation:**
- API Docs: `http://localhost:8000/docs`
- Ollama Docs: https://ollama.com/
- FastAPI Docs: https://fastapi.tiangolo.com/

---

**🎉 Hoàn thành! API đã production-ready với đầy đủ requirements từ docx.**

## API Endpoints

### Health

- `GET /health/live` - Liveness probe (returns 200 if server is running)
- `GET /health/ready` - Readiness probe (checks Ollama and model availability)

### Generation

- `POST /v1/generate` - Generate text from a prompt
  ```json
  {
    "prompt": "Your prompt here",
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 200
  }
  ```

### Chat

- `POST /v1/chat` - Multi-turn chat (stateless - provide full history)
  ```json
  {
    "messages": [
      {"role": "user", "content": "Hello"},
      {"role": "assistant", "content": "Hi there!"},
      {"role": "user", "content": "How are you?"}
    ],
    "temperature": 0.7,
    "max_tokens": 300
  }
  ```

## Configuration

All configuration is done via environment variables (see `.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_NAME` | `qwen3.5:4b` | Ollama model to use |
| `OLLAMA_URL` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_TIMEOUT` | `120` | Timeout in seconds |
| `API_HOST` | `0.0.0.0` | API server host |
| `API_PORT` | `8000` | API server port |
| `DEFAULT_TEMPERATURE` | `0.7` | Default sampling temperature |
| `DEFAULT_TOP_P` | `0.9` | Default nucleus sampling |
| `DEFAULT_MAX_TOKENS` | `200` | Default max tokens |
| `LOG_LEVEL` | `INFO` | Logging level |
| `LOG_REQUEST_ID` | `true` | Log request IDs |
| `LOG_PROMPTS` | `false` | Log prompts (privacy) |
| `ENABLE_METRICS` | `true` | Enable TTFT/TBT metrics |

## Error Handling

The API returns appropriate HTTP status codes:

- `200` - Success
- `404` - Model not found
- `503` - Ollama unavailable
- `504` - Request timeout
- `500` - Internal server error

All errors include a descriptive message in the response body.

## Development

### Run Tests

```bash
pip install -e ".[test]"
pytest tests/
```

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

This includes both API and test dependencies.

## Production Deployment

### Docker (Recommended)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir ".[api]"

ENV OLLAMA_URL=http://ollama:11434
EXPOSE 8000

CMD ["python", "-m", "api.main"]
```

### Kubernetes

Use `/health/live` for liveness probe and `/health/ready` for readiness probe:

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 30

readinessProbe:
  httpGet:
    path: /health/ready
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
```

## Metrics

When `ENABLE_METRICS=true`, the API tracks:

- **TTFT**: Time to First Token (milliseconds)
- **TBT**: Average Time Between Tokens (milliseconds)
- **Throughput**: Tokens per second
- **Latency**: Total request time

Metrics are included in the response when available.

## License

MIT License - See LICENSE file for details.
