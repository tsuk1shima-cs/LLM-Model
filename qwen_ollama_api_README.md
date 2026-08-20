# Qwen 3.5 4B API với Theo Dõi Chỉ Số Nâng Cao

API server FastAPI toàn diện cho Qwen 3.5 4B với theo dõi TTFT, TBT, và Throughput.

---

## 📋 Tổng Quan

**File:** `qwen_ollama_api.py`  
**Framework:** FastAPI  
**Mô hình:** Qwen 3.5 4B (qwen3.5:4b)  
**Port:** 8000  

### Tính Năng Chính

- ✅ **Sinh văn bản** với hoặc không streaming
- ✅ **Chat nhiều lượt** với context
- ✅ **Theo dõi chỉ số nâng cao** (TTFT, TBT, Throughput)
- ✅ **Phân tích hiệu suất** chi tiết
- ✅ **Xuất CSV** tự động
- ✅ **Health check** và thông tin mô hình
- ✅ **API documentation** tự động (OpenAPI/Swagger)

---

## 🚀 Cài Đặt và Chạy

### Yêu Cầu

```bash
# Python 3.8+
# Ollama đã cài đặt và chạy
# Qwen 3.5 4B đã tải xuống
```

### Cài Đặt Dependencies

```bash
pip install fastapi uvicorn ollama pandas
```

### Chạy Server

```bash
python qwen_ollama_api.py
```

Server sẽ chạy tại: **http://localhost:8000**

### Truy Cập Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 📚 API Endpoints

### 1. Root Endpoint

```
GET /
```

Thông tin API và danh sách endpoints.

**Response:**
```json
{
  "name": "Qwen 3.5 4B API with Advanced Metrics",
  "version": "2.0.0",
  "model": "qwen3.5:4b",
  "features": [...],
  "endpoints": {...}
}
```

---

### 2. Health Check

```
GET /health
```

Kiểm tra trạng thái server và kết nối mô hình.

**Response:**
```json
{
  "status": "healthy",
  "model": "qwen3.5:4b",
  "timestamp": "2026-08-20T14:30:45",
  "metrics_count": 42
}
```

---

### 3. Sinh Văn Bản

```
POST /api/generate
```

Sinh văn bản từ prompt với theo dõi chỉ số tùy chọn.

**Request Body:**
```json
{
  "prompt": "What is artificial intelligence?",
  "temperature": 0.7,
  "top_p": 0.9,
  "max_tokens": 200,
  "stream": false,
  "track_metrics": true
}
```

**Response:**
```json
{
  "response": "Artificial Intelligence (AI) is...",
  "model": "qwen3.5:4b",
  "metrics": {
    "ttft_ms": 85.3,
    "avg_tbt_ms": 18.2,
    "total_time": 2.45,
    "tokens_per_second": 48.9,
    "output_tokens": 120,
    "total_tokens": 135,
    "speed_rating": "⚡ Very Good"
  },
  "timestamp": "2026-08-20T14:30:45"
}
```

**Parameters:**

- `prompt` (required): Text prompt
- `temperature` (optional): 0.0-2.0, mặc định 0.7
- `top_p` (optional): 0.0-1.0, mặc định 0.9
- `max_tokens` (optional): 1-4096, mặc định 200
- `stream` (optional): true/false, mặc định false
- `track_metrics` (optional): true/false, mặc định true

---

### 4. Chat Conversation

```
POST /api/chat
```

Cuộc trò chuyện nhiều lượt với context.

**Request Body:**
```json
{
  "messages": [
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi! How can I help?"},
    {"role": "user", "content": "What is machine learning?"}
  ],
  "temperature": 0.7,
  "top_p": 0.9,
  "max_tokens": 300
}
```

**Response:**
```json
{
  "message": {
    "role": "assistant",
    "content": "Machine learning is..."
  },
  "model": "qwen3.5:4b",
  "timestamp": "2026-08-20T14:30:45"
}
```

---

### 5. Xem Chỉ Số

```
GET /api/metrics
```

Lấy tóm tắt chỉ số và dữ liệu hiệu suất gần đây.

**Response:**
```json
{
  "summary": {
    "total_requests": 42,
    "avg_ttft_ms": 89.5,
    "avg_tbt_ms": 19.3,
    "avg_total_time": 2.56,
    "avg_tokens_per_sec": 47.2,
    "min_ttft_ms": 75.0,
    "max_ttft_ms": 120.0,
    "total_tokens": 5040
  },
  "total_metrics": 42,
  "recent_metrics": [...]
}
```

---

### 6. Xuất Chỉ Số

```
GET /api/metrics/export
```

Tải xuống file CSV chứa tất cả chỉ số.

**Response:** File CSV

**Columns:**
- timestamp
- prompt
- response
- ttft, avg_tbt, total_time
- prompt_tokens, output_tokens, total_tokens
- tokens_per_second
- ttft_ms, avg_tbt_ms
- model, temperature, top_p, max_tokens

---

### 7. Xóa Chỉ Số

```
DELETE /api/metrics
```

Xóa tất cả chỉ số đã thu thập.

**Response:**
```json
{
  "message": "Cleared 42 metrics",
  "timestamp": "2026-08-20T14:30:45"
}
```

---

### 8. Thông Tin Mô Hình

```
GET /api/model/info
```

Lấy thông tin về mô hình Qwen 3.5 4B.

**Response:**
```json
{
  "model": "qwen3.5:4b",
  "version": "3.5",
  "size": "~2.5GB",
  "context_window": 128000,
  "parameters": "4 billion",
  "description": "Qwen 3.5 4B with Hybrid Gated Delta Networks architecture"
}
```

---

## 💡 Ví Dụ Sử Dụng

### Python (requests)

```python
import requests

# 1. Health check
response = requests.get("http://localhost:8000/health")
print(response.json())

# 2. Generate text with metrics
response = requests.post(
    "http://localhost:8000/api/generate",
    json={
        "prompt": "What is AI?",
        "temperature": 0.7,
        "max_tokens": 200,
        "track_metrics": True
    }
)
result = response.json()
print(f"Response: {result['response']}")
print(f"Speed: {result['metrics']['tokens_per_second']} tok/s")

# 3. Chat conversation
response = requests.post(
    "http://localhost:8000/api/chat",
    json={
        "messages": [
            {"role": "user", "content": "Hello!"},
            {"role": "assistant", "content": "Hi there!"},
            {"role": "user", "content": "Tell me about Python"}
        ]
    }
)
print(response.json()['message']['content'])

# 4. Get metrics
response = requests.get("http://localhost:8000/api/metrics")
metrics = response.json()
print(f"Total requests: {metrics['total_metrics']}")
print(f"Avg speed: {metrics['summary']['avg_tokens_per_sec']:.2f} tok/s")
```

### cURL

```bash
# Health check
curl http://localhost:8000/health

# Generate text
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What is AI?",
    "temperature": 0.7,
    "max_tokens": 200,
    "track_metrics": true
  }'

# Chat
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'

# Get metrics
curl http://localhost:8000/api/metrics

# Export metrics
curl http://localhost:8000/api/metrics/export -o metrics.csv
```

### JavaScript (fetch)

```javascript
// Generate text
const response = await fetch('http://localhost:8000/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: 'What is AI?',
    temperature: 0.7,
    max_tokens: 200,
    track_metrics: true
  })
});

const result = await response.json();
console.log('Response:', result.response);
console.log('Metrics:', result.metrics);
```

---

## 📊 Chỉ Số Được Theo Dõi

### TTFT (Time To First Token)

**Định nghĩa**: Thời gian từ khi gửi request đến khi nhận token đầu tiên

**Thang đo**:
- 🔥 Xuất sắc: < 100ms
- ⚡ Rất tốt: 100-200ms
- ✅ Tốt: 200-300ms
- ⚠️ Khá: 300-500ms
- 🐌 Chậm: > 500ms

### TBT (Time Between Tokens)

**Định nghĩa**: Thời gian trung bình giữa các token liên tiếp

**Thang đo**:
- 🔥 Xuất sắc: < 15ms
- ⚡ Rất tốt: 15-20ms
- ✅ Tốt: 20-25ms
- ⚠️ Khá: 25-30ms
- 🐌 Chậm: > 30ms

### Throughput (Tokens/Second)

**Định nghĩa**: Số token được tạo ra mỗi giây

**Thang đo**:
- 🔥 Xuất sắc: > 60 tok/s
- ⚡ Rất tốt: 40-60 tok/s
- ✅ Tốt: 25-40 tok/s
- ⚠️ Khá: 15-25 tok/s
- 🐌 Chậm: < 15 tok/s

---

## 🔧 Configuration

### Thay Đổi Port

```python
# Trong file qwen_ollama_api.py, dòng cuối:
uvicorn.run(
    app,
    host="0.0.0.0",
    port=8080,  # Thay đổi port
    log_level="info"
)
```

### Thay Đổi Mô Hình

```python
# Trong file qwen_ollama_api.py, đầu file:
MODEL_NAME = "qwen3.5:7b"  # Thay đổi mô hình
```

### Thay Đổi Giá Trị Mặc Định

```python
DEFAULT_TEMPERATURE = 0.5
DEFAULT_TOP_P = 0.95
DEFAULT_MAX_TOKENS = 500
```

---

## 🔐 Bảo Mật

### Production Deployment

1. **CORS**: Cập nhật `allow_origins` để chỉ định domain cụ thể

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Cụ thể hóa
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Authentication**: Thêm API key hoặc OAuth2

3. **Rate Limiting**: Sử dụng middleware để giới hạn requests

4. **HTTPS**: Chạy sau reverse proxy (nginx, caddy)

---

## 📈 Hiệu Suất

### Trên GPU Tesla T4

- **TTFT**: 80-120 ms (típico)
- **TBT**: 18-25 ms (típico)
- **Throughput**: 35-55 tokens/giây
- **Memory**: ~3GB VRAM

### Tối Ưu Hóa

1. **Giảm max_tokens**: Giảm độ dài đầu ra
2. **Batch requests**: Xử lý nhiều requests cùng lúc
3. **Cache results**: Cache các response phổ biến
4. **Use faster model**: Thử `qwen3.5:3b` cho tốc độ cao hơn

---

## 🐛 Xử Lý Lỗi

### Lỗi Thường Gặp

#### 1. "Service unavailable"

**Nguyên nhân**: Ollama không chạy hoặc mô hình chưa tải

**Giải pháp**:
```bash
# Kiểm tra Ollama
ollama list

# Tải mô hình
ollama pull qwen3.5:4b

# Chạy Ollama
ollama serve
```

#### 2. "Connection refused"

**Nguyên nhân**: Cổng 8000 đã được sử dụng

**Giải pháp**: Thay đổi port hoặc kill process đang dùng port

#### 3. "Out of memory"

**Nguyên nhân**: Không đủ VRAM

**Giải pháp**: Sử dụng mô hình nhỏ hơn (`qwen3.5:3b`)

---

## 📁 Cấu Trúc File

```
qwen_ollama_api.py          # API server chính
qwen_ollama_api_README.md   # Documentation này
qwen_metrics_*.csv          # File CSV xuất ra
```

---

## 🔄 So Sánh với qwen_api.py

### qwen_api.py (Cơ bản)

- ✅ Endpoints cơ bản (/generate, /chat)
- ✅ Simple metrics (total time, tokens)
- ❌ Không có TTFT tracking
- ❌ Không có TBT tracking
- ❌ Không có metrics export

### qwen_ollama_api.py (Nâng cao) ⭐

- ✅ Tất cả endpoints của bản cơ bản
- ✅ **TTFT tracking** chi tiết
- ✅ **TBT tracking** chi tiết
- ✅ **Throughput monitoring**
- ✅ **Metrics export** (CSV)
- ✅ **Performance analytics**
- ✅ **Speed ratings**
- ✅ **Recent metrics** view

---

## 🚀 Deployment

### Local Development

```bash
python qwen_ollama_api.py
```

### Production (với Uvicorn)

```bash
uvicorn qwen_ollama_api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY qwen_ollama_api.py .

CMD ["uvicorn", "qwen_ollama_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Với Nginx (Reverse Proxy)

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📝 Logs

API tự động log các sự kiện quan trọng:

```
2026-08-20 14:30:45 - INFO - Starting Qwen 3.5 4B API Server
2026-08-20 14:30:50 - INFO - Generate request: prompt length=50
2026-08-20 14:30:50 - INFO - First token received in 85.30ms
2026-08-20 14:30:52 - INFO - Generation completed - TTFT: 85.30ms, Speed: 48.90 tok/s
```

---

## 🎯 Use Cases

### 1. Chatbot Backend

```python
# Chat với context memory
messages = []
while True:
    user_input = input("You: ")
    messages.append({"role": "user", "content": user_input})
    
    response = requests.post(
        "http://localhost:8000/api/chat",
        json={"messages": messages}
    )
    
    assistant_msg = response.json()['message']
    messages.append(assistant_msg)
    print(f"Bot: {assistant_msg['content']}")
```

### 2. Content Generation

```python
def generate_article(topic):
    response = requests.post(
        "http://localhost:8000/api/generate",
        json={
            "prompt": f"Write an article about {topic}",
            "temperature": 0.8,
            "max_tokens": 1000
        }
    )
    return response.json()['response']
```

### 3. Performance Monitoring

```python
import time

# Monitor performance over time
while True:
    metrics = requests.get("http://localhost:8000/api/metrics").json()
    print(f"Avg Speed: {metrics['summary']['avg_tokens_per_sec']:.2f} tok/s")
    time.sleep(60)  # Check every minute
```

---

## 🔗 Liên Kết

### API Related

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Uvicorn**: https://www.uvicorn.org/
- **Ollama Python**: https://github.com/ollama/ollama-python

### Model Related

- **Qwen 3.5 4B**: https://ollama.com/library/qwen3.5:4b
- **Qwen GitHub**: https://github.com/QwenLM/Qwen
- **Ollama**: https://ollama.com/

---

## 📞 Support

Đối với các vấn đề hoặc câu hỏi:

1. Kiểm tra logs của API
2. Xem phần Troubleshooting
3. Kiểm tra Ollama đang chạy
4. Đảm bảo mô hình đã tải

---

**Phiên Bản**: 2.0.0  
**Ngày Cập Nhật**: 20 Tháng 8, 2026  
**Trạng Thái**: Production Ready ✅

**Tính Năng Nổi Bật**:
- 📊 Advanced Metrics Tracking
- ⚡ TTFT & TBT Monitoring
- 🚀 High Performance
- 📈 Analytics Ready

---

**Chúc Bạn Sử Dụng Vui Vẻ! 🚀**
