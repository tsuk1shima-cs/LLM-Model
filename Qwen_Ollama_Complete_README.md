# Qwen 3.5 4B với Ollama + Theo Dõi Chỉ Số Nâng Cao

Notebook Google Colab toàn diện để chạy mô hình ngôn ngữ Qwen 3.5 4B với theo dõi chỉ số hiệu suất nâng cao, trực quan hóa và khả năng xuất dữ liệu.

---

## 📋 Tổng Quan

**File:** `Qwen_Ollama_Complete.ipynb`  
**Nền tảng:** Google Colab  
**Mô hình:** Qwen 3.5 4B (qwen3.5:4b)  
**Tổng số bước:** 20 bước (44 cells)  
**Thời gian ước tính:** 15-20 phút  

### Notebook Này Làm Gì

Notebook này cung cấp thiết lập hoàn chỉnh để chạy và đánh giá mô hình ngôn ngữ Qwen 3.5 4B với theo dõi hiệu suất chi tiết:

- ✅ **Cài đặt và cấu hình Ollama** trên Google Colab
- ✅ **Tải xuống mô hình Qwen 3.5 4B** (~2.5GB, định dạng tối ưu)
- ✅ **Theo dõi chỉ số nâng cao** với TTFT, TBT, và Throughput
- ✅ **Trực quan hóa hiệu suất** với bảng điều khiển 6 biểu đồ
- ✅ **Nhiều kịch bản kiểm tra** để đánh giá toàn diện
- ✅ **Xuất CSV** để phân tích thêm
- ✅ **Giao diện chat** cho các cuộc trò chuyện nhiều lượt
- ✅ **Kiểm tra tham số** (temperature, top-p)

---

## 🚀 Bắt Đầu Nhanh

### 1. Tải Lên Google Colab

1. Truy cập [Google Colab](https://colab.research.google.com/)
2. File → Upload notebook
3. Chọn `Qwen_Ollama_Complete.ipynb`

### 2. Chọn GPU Runtime

1. Runtime → Change runtime type
2. Hardware accelerator: **GPU (T4)**
3. Nhấn Save

### 3. Chạy Tất Cả Cells

1. Runtime → Run all
2. Chờ hoàn thành (~15-20 phút)
3. Xem lại chỉ số và trực quan hóa

---

## 📊 Tính Năng Chính

### 1. **Theo Dõi Chỉ Số Nâng Cao**

Notebook bao gồm lớp `AdvancedMetricsTracker` toàn diện để đo lường:

- **TTFT (Time To First Token)**: Độ trễ từ yêu cầu đến token đầu tiên
  - Mục tiêu: <100ms (Xuất sắc)
  - Đo bằng mili giây
  
- **TBT (Time Between Tokens)**: Thời gian trung bình giữa các token liên tiếp
  - Mục tiêu: <20ms (Rất tốt)
  - Cho biết tính nhất quán trong sinh token
  
- **Throughput**: Số token được tạo ra mỗi giây
  - Mục tiêu: >40 tok/s (Tốt trên T4)
  - Chỉ số tốc độ tổng thể

### 2. **Bảng Điều Khiển Hiệu Suất**

Bảng điều khiển trực quan hóa 6 biểu đồ hiển thị:

1. **TTFT Theo Thời Gian** - Biểu đồ đường theo dõi độ trễ token đầu tiên
2. **TBT Theo Thời Gian** - Biểu đồ đường hiển thị tính nhất quán tạo token
3. **Throughput** - Biểu đồ cột số token mỗi giây
4. **Tổng Thời Gian** - Biểu đồ đường thời gian tạo hoàn chỉnh
5. **Số Token Đầu Ra** - Biểu đồ cột token mỗi yêu cầu
6. **TTFT vs Tokens** - Biểu đồ phân tán hiển thị tương quan

### 3. **Khả Năng Xuất Dữ Liệu**

- **Xuất CSV**: Tất cả chỉ số được lưu với dấu thời gian
- **Xuất Google Sheets**: Tích hợp trực tiếp (tùy chọn)
- **Tự động tải xuống**: File tự động tải xuống từ Colab

---

## 📚 Cấu Trúc Notebook

### Phần 1: Thiết Lập (Bước 1-7)

| Bước | Mô Tả | Thời Gian |
|------|-------|-----------|
| 1 | Cài đặt Ollama trên Colab | 1-2 phút |
| 2 | Xác minh cài đặt | 5 giây |
| 3 | Kiểm tra GPU có sẵn | 5 giây |
| 4 | Khởi động Ollama Server | 5-10 giây |
| 5 | Tải xuống mô hình Qwen 3.5 4B | 2-3 phút |
| 6 | Liệt kê các mô hình có sẵn | 2 giây |
| 7 | Cài đặt thư viện Python | 30 giây |

### Phần 2: Hệ Thống Chỉ Số (Bước 8-13)

| Bước | Mô Tả | Kết Quả |
|------|-------|---------|
| 8 | Thiết lập Advanced Metrics Tracker | Khởi tạo lớp tracker |
| 9 | Kiểm tra sinh văn bản với chỉ số | Kiểm tra đơn với chỉ số đầy đủ |
| 10 | Chạy nhiều kiểm tra | 6 prompt đa dạng được benchmark |
| 11 | Trực quan hóa bảng điều khiển | Bảng điều khiển 6 biểu đồ |
| 12 | Xuất ra CSV | File CSV với tất cả chỉ số |
| 13 | Xuất ra Google Sheets (Tùy chọn) | Bảng tính trực tuyến |

### Phần 3: Kiểm Tra & Khám Phá (Bước 14-20)

| Bước | Mô Tả | Mục Đích |
|------|-------|----------|
| 14 | Kiểm tra sinh văn bản cơ bản | Kiểm tra sinh đơn giản |
| 15 | Sinh theo luồng (Streaming) | Đầu ra token-by-token thời gian thực |
| 16 | Giao diện chat | Cuộc trò chuyện nhiều lượt |
| 17 | Hàm chat tùy chỉnh | Hỏi đáp tương tác |
| 18 | Tùy chọn nâng cao | Kiểm tra Temperature/Top-P |
| 19 | Đánh giá hiệu suất | Kiểm tra tốc độ trên các prompt |
| 20 | Thông tin mô hình | Xem thông số kỹ thuật mô hình |

---

## 🎯 Thông Tin Mô Hình

### Thông Số Kỹ Thuật Qwen 3.5 4B

- **Model ID**: `qwen3.5:4b`
- **Tham số**: 4 tỷ
- **Kiến trúc**: Hybrid Gated Delta Networks
- **Cửa sổ ngữ cảnh**: 128,000 tokens (128K)
- **Kích thước tải xuống**: ~2.5GB (định dạng GGUF)
- **Sử dụng VRAM**: ~3GB trong quá trình suy luận
- **Dữ liệu huấn luyện**: Đến Q4 2024

### Hiệu Suất Trên GPU Tesla T4

- **TTFT**: 80-120 ms (thông thường)
- **TBT**: 18-25 ms (thông thường)
- **Throughput**: 35-55 tokens/giây
- **Đánh giá tốc độ**: Rất tốt đến Xuất sắc

### Cải Tiến So Với Qwen 2.5

- 📈 **Lý luận tốt hơn 15-20%** trên các benchmark toán học
- 🎨 **Hiểu đa phương thức tăng cường**
- 📝 **Tuân theo hướng dẫn chính xác hơn**
- 🔄 **Cửa sổ ngữ cảnh lớn gấp 4 lần** (32K → 128K)
- ⚡ **Suy luận nhanh hơn 10-15%**

### Các Biến Thể Mô Hình Có Sẵn

```
qwen3.5:0.5b  → 500MB  |  80-120 tok/s  |  Siêu nhẹ
qwen3.5:1.5b  → 1GB    |  60-90 tok/s   |  Nhỏ & nhanh
qwen3.5:3b    → 2GB    |  45-65 tok/s   |  Cân bằng
qwen3.5:4b    → 2.5GB  |  35-55 tok/s   |  ⭐ MẶC ĐỊNH
qwen3.5:7b    → 4.5GB  |  25-40 tok/s   |  Chất lượng cao
qwen3.5:14b   → 9GB    |  15-25 tok/s   |  Hiệu suất tốt nhất
```

---

## 📦 Yêu Cầu

### Yêu Cầu Nền Tảng

- **Google Colab** (Miễn phí hoặc Pro)
- **GPU Runtime**: Tesla T4 (15GB VRAM) - Miễn phí với Colab
- **RAM**: ~12.67 GB RAM hệ thống
- **Lưu trữ**: ~10GB dung lượng trống (cho mô hình và file tạm)

### Thư Viện Python (Tự động cài đặt)

- **ollama** - Client Python chính thức của Ollama
- **requests** - Thư viện HTTP
- **pandas** - Thao tác dữ liệu và xuất CSV
- **matplotlib** - Trực quan hóa và biểu đồ
- **gspread** - Google Sheets API (tùy chọn)
- **oauth2client** - Google OAuth (tùy chọn)

### Gói Hệ Thống (Tự động cài đặt)

- **pciutils** - Tiện ích phát hiện GPU
- **zstd** - Tiện ích nén
- **CUDA** - Đã cài đặt sẵn trên Colab

---

## 💡 Ví Dụ Sử Dụng

### Ví Dụ 1: Kiểm Tra Đơn Nhanh

**Mô tả**: Sinh văn bản đơn giản với một câu hỏi.

### Ví Dụ 2: Với Theo Dõi Chỉ Số

**Mô tả**: Khởi tạo tracker và đo lường quá trình sinh văn bản với các chỉ số chi tiết.

### Ví Dụ 3: Cuộc Trò Chuyện Chat

**Mô tả**: Tạo cuộc trò chuyện nhiều lượt với context được duy trì qua các message.

### Ví Dụ 4: Đầu Ra Theo Luồng

**Mô tả**: Hiển thị token theo thời gian thực trong quá trình sinh.

### Ví Dụ 5: Kiểm Soát Temperature

**Mô tả**: 
- **Bảo thủ (temperature thấp)**: Cho câu trả lời xác định, tập trung
- **Sáng tạo (temperature cao)**: Cho câu trả lời đa dạng, sáng tạo

---

## 📊 Giải Thích Các Chỉ Số

### TTFT (Time To First Token)

**Định nghĩa**: Thời gian từ khi gửi yêu cầu đến khi nhận token đầu tiên

**Tầm quan trọng**: 
- Ảnh hưởng đến độ trễ cảm nhận
- Quan trọng cho ứng dụng thời gian thực
- Chỉ số trải nghiệm người dùng

**Thang Đánh Giá**:
```
🔥 Xuất sắc:   < 100ms
⚡ Rất tốt:    100-200ms
✅ Tốt:        200-300ms
⚠️  Khá:       300-500ms
🐌 Chậm:       > 500ms
```

**Các Yếu Tố Ảnh Hưởng Đến TTFT**:
- Kích thước mô hình (lớn hơn = chậm hơn)
- Độ dài prompt (dài hơn = chậm hơn)
- Tốc độ GPU (GPU nhanh hơn = TTFT nhanh hơn)
- Tải server (bận hơn = chậm hơn)

### TBT (Time Between Tokens)

**Định nghĩa**: Thời gian trung bình giữa các lần tạo token liên tiếp

**Tầm quan trọng**:
- Cho biết tính mượt mà của việc sinh
- Ảnh hưởng đến trải nghiệm streaming
- Hiển thị tính nhất quán

**Thang Đánh Giá**:
```
🔥 Xuất sắc:   < 15ms
⚡ Rất tốt:    15-20ms
✅ Tốt:        20-25ms
⚠️  Khá:       25-30ms
🐌 Chậm:       > 30ms
```

**Đặc điểm**:
- Thường ổn định hơn TTFT
- Ít phương sai giữa các yêu cầu
- Chủ yếu phụ thuộc vào phần cứng

### Throughput (Token Mỗi Giây)

**Định nghĩa**: Tổng số token được tạo ra mỗi giây

**Công thức**: `số_token_đầu_ra / tổng_thời_gian`

**Tầm quan trọng**:
- Chỉ số tốc độ tổng thể
- Lập kế hoạch công suất
- So sánh mô hình

**Thang Đánh Giá**:
```
🔥 Xuất sắc:   > 60 tok/s
⚡ Rất tốt:    40-60 tok/s
✅ Tốt:        25-40 tok/s
⚠️  Khá:       15-25 tok/s
🐌 Chậm:       < 15 tok/s
```

---

## 📁 File Đầu Ra

### Định Dạng Xuất CSV

**Tên file**: `qwen_metrics_YYYYMMDD_HHMMSS.csv`

**Các cột**:
- **timestamp**: Dấu thời gian (ví dụ: "2026-08-20 14:30:45")
- **model**: Tên mô hình ("qwen3.5:4b")
- **prompt**: 100 ký tự đầu của prompt
- **response**: 200 ký tự đầu của câu trả lời
- **ttft**: Thời gian đến token đầu tiên (giây)
- **avg_tbt**: Thời gian trung bình giữa các token (giây)
- **total_time**: Tổng thời gian sinh (giây)
- **prompt_tokens**: Số token đầu vào
- **output_tokens**: Số token đầu ra
- **total_tokens**: Tổng token (đầu vào + đầu ra)
- **tokens_per_second**: Chỉ số throughput
- **ttft_ms**: TTFT tính bằng mili giây
- **avg_tbt_ms**: TBT tính bằng mili giây
- **temperature**: Giá trị temperature được sử dụng
- **top_p**: Giá trị top-p được sử dụng
- **max_tokens**: Giá trị max tokens

### Trực Quan Hóa

**Các Biểu Đồ Dashboard** (PNG hoặc hiển thị trong notebook):
1. **ttft_over_time.png** - Biểu đồ đường TTFT
2. **tbt_over_time.png** - Biểu đồ đường TBT
3. **throughput.png** - Biểu đồ cột Throughput
4. **total_time.png** - Biểu đồ đường Tổng thời gian
5. **output_tokens.png** - Biểu đồ cột Số token
6. **ttft_vs_tokens.png** - Biểu đồ phân tán tương quan

---

## ⚙️ Tùy Chọn Cấu Hình

### Tham Số Mô Hình

**Temperature**: Kiểm soát tính ngẫu nhiên
- `0.0` = Xác định, tập trung
- `0.7` = Mặc định, cân bằng
- `1.0` = Cân bằng
- `2.0` = Rất sáng tạo, ngẫu nhiên

**Top-P**: Lấy mẫu nucleus
- `0.5` = Lấy mẫu bảo thủ
- `0.9` = Mặc định, cân bằng
- `1.0` = Lấy mẫu từ tất cả token

**Max Tokens**: Giới hạn độ dài đầu ra
- `200` = Mặc định
- Đặt dựa trên độ dài phản hồi mong muốn

**Top-K**: Thay thế cho top-p
- `40` = Tùy chọn
- Giới hạn lấy mẫu đến K token hàng đầu

### Tùy Chọn Sinh

Các tham số có thể điều chỉnh:
- **temperature**: Kiểm soát độ ngẫu nhiên
- **top_p**: Lấy mẫu nucleus
- **top_k**: Giới hạn sampling
- **num_predict**: Số token tối đa
- **num_ctx**: Cửa sổ ngữ cảnh
- **repeat_penalty**: Phạt lặp lại
- **stop**: Chuỗi dừng

---

## 🔧 Khắc Phục Sự Cố

### Các Vấn Đề Thường Gặp và Giải Pháp

#### 1. GPU Không Khả Dụng

**Vấn đề**: Thông báo "No GPU detected"

**Giải pháp**:
1. Runtime → Change runtime type
2. Hardware accelerator → GPU
3. Lưu và khởi động lại runtime

#### 2. Cài Đặt Ollama Thất Bại

**Vấn đề**: Lỗi `curl: command not found` hoặc lỗi cài đặt

**Giải pháp**: Thử cài đặt lại với apt-get update trước

#### 3. Tải Mô Hình Chậm

**Vấn đề**: Tải xuống mất >10 phút

**Giải pháp**:
- **Đợi kiên nhẫn**: 2.5GB thường mất 2-5 phút
- **Kiểm tra mạng**: Tốc độ mạng Colab thay đổi
- **Khởi động lại runtime**: Đôi khi có hiệu quả
- **Thử mô hình nhỏ hơn**: Sử dụng `qwen3.5:3b`

#### 4. Server Không Khởi Động

**Vấn đề**: "Connection refused" hoặc timeout

**Giải pháp**: Kill và khởi động lại Ollama server

#### 5. Hết Bộ Nhớ

**Vấn đề**: Lỗi CUDA out of memory

**Giải pháp**:
- **Khởi động lại runtime**: Runtime → Restart runtime
- **Dùng mô hình nhỏ hơn**: Chuyển sang `qwen3.5:3b`
- **Giảm max_tokens**: Giảm độ dài đầu ra
- **Đóng các tab khác**: Giải phóng tài nguyên hệ thống

#### 6. Sinh Chậm

**Vấn đề**: Tốc độ <15 tok/s

**Nguyên nhân & Giải pháp**:
- **Không có GPU**: Bật GPU runtime
- **Prompt lớn**: Rút ngắn đầu vào
- **Temperature cao**: Giảm xuống 0.3-0.5
- **Server bận**: Khởi động lại Ollama

#### 7. CSV Không Tải Xuống

**Vấn đề**: File không tải xuống từ Colab

**Giải pháp**: Tải xuống thủ công hoặc kiểm tra file có tồn tại

---

## 📈 Tối Ưu Hóa Hiệu Suất

### Tối Ưu Tốc Độ

**Để Sinh Nhanh Hơn**:
- Sử dụng temperature thấp (0.1)
- Giảm max tokens (100)
- Dùng mô hình nhỏ hơn (`qwen3.5:3b`)
- Prompt ngắn hơn

### Tối Ưu Chất Lượng

**Để Phản Hồi Tốt Hơn**:
- Sử dụng temperature cao hơn cho sáng tạo (0.8)
- Tăng max tokens (500)
- Dùng mô hình lớn hơn (`qwen3.5:7b`)
- Prompt chi tiết hơn

### Cài Đặt Cân Bằng

**Đề Xuất Cho Hầu Hết Trường Hợp**:
- **temperature**: 0.7 (Sáng tạo cân bằng)
- **top_p**: 0.9 (Đa dạng tốt)
- **max_tokens**: 200 (Độ dài hợp lý)

---

## 🎓 Thực Hành Tốt Nhất

### 1. Bắt Đầu Với Cài Đặt Mặc Định

- Sử dụng `qwen3.5:4b` (cân bằng tốt nhất)
- Temperature: 0.7
- Max tokens: 200
- Đánh giá, sau đó điều chỉnh

### 2. Phù Hợp Temperature Với Nhiệm Vụ

| Nhiệm Vụ | Temperature | Lý Do |
|----------|-------------|-------|
| Toán/Lập trình | 0.1-0.3 | Cần độ chính xác |
| Hỏi đáp | 0.5-0.7 | Cân bằng |
| Viết sáng tạo | 0.8-1.2 | Cần đa dạng |
| Brainstorming | 1.0-1.5 | Đa dạng tối đa |

### 3. Giám Sát Chỉ Số

- Kiểm tra TTFT cho vấn đề độ trễ
- Theo dõi TBT cho tính nhất quán
- Theo dõi throughput cho lập kế hoạch công suất
- Xuất chỉ số để phân tích

### 4. Nhóm Các Yêu Cầu Tương Tự

- Nhóm câu hỏi theo loại
- Chạy tất cả cùng lúc
- Phân tích mẫu trong kết quả

### 5. Lưu Kết Quả

- Luôn xuất CSV
- Giữ trực quan hóa
- Ghi chép cài đặt đã sử dụng
- Theo dõi thay đổi theo thời gian

---

## 📖 Tài Nguyên Bổ Sung

### Tài Liệu Chính Thức

- **Ollama**: https://ollama.com/
- **Ollama Docs**: https://ollama.com/docs
- **Qwen 3.5**: https://ollama.com/library/qwen3.5
- **Qwen 3.5 4B**: https://ollama.com/library/qwen3.5:4b

### Tài Nguyên Qwen

- **GitHub**: https://github.com/QwenLM/Qwen
- **HuggingFace**: https://huggingface.co/Qwen
- **Blog**: https://qwenlm.github.io/

### File Liên Quan

- **Bộ Đầy Đủ**: `Qwen_Complete_Evaluation_Suite.ipynb`
- **API Server**: `qwen_api.py` + `API_README.txt`
- **Tài Liệu Đầy Đủ**: `Complete_Documentation.txt`
- **Hướng Dẫn Nhanh**: `README.txt`

---

## 🤝 Hỗ Trợ

### Nhận Trợ Giúp

1. **Đọc phần khắc phục sự cố** ở trên
2. **Kiểm tra tài liệu Ollama**: https://ollama.com/docs
3. **Xem lại thông báo lỗi** cẩn thận
4. **Khởi động lại runtime** là bước đầu tiên

### Tài Nguyên Hỗ Trợ Thường Dùng

- **Ollama Discord**: https://discord.gg/ollama
- **GitHub Issues**: https://github.com/ollama/ollama/issues
- **Qwen Discussions**: https://huggingface.co/Qwen

---

## 📝 Ghi Chú

### Những Điều Cần Lưu Ý

1. **Giới Hạn Colab Miễn Phí**:
   - Thời gian chờ phiên 12 giờ
   - Có thể ngắt kết nối khi không hoạt động
   - GPU không phải lúc nào cũng có sẵn
   - Cân nhắc Colab Pro để độ tin cậy cao hơn

2. **Lưu Trữ Mô Hình**:
   - Mô hình bị xóa khi runtime dừng
   - Phải tải lại khi khởi động lại
   - Mất 2-3 phút mỗi lần

3. **Độ Chính Xác Chỉ Số**:
   - TTFT rất chính xác (đo trực tiếp)
   - TBT đo giữa các chunk
   - Số token là ước tính
   - Tốc độ thay đổi theo prompt

4. **Quyền Riêng Tư**:
   - Tất cả xử lý cục bộ trên Colab
   - Không gửi dữ liệu đến API bên ngoài
   - Mô hình chạy trên server Google
   - Áp dụng điều khoản Colab tiêu chuẩn

---

## 📄 Giấy Phép

Notebook này được cung cấp nguyên trạng cho mục đích giáo dục và nghiên cứu.

**Các Thành Phần**:
- Ollama: Giấy phép MIT
- Qwen 3.5 4B: Giấy phép Apache 2.0
- Thư viện Python: Nhiều giấy phép mã nguồn mở

---

## ✅ Danh Sách Kiểm Tra

Trước khi chạy notebook:

- [ ] Tài khoản Google có quyền truy cập Colab
- [ ] Đã chọn GPU runtime (T4)
- [ ] Kết nối internet tốt
- [ ] Có 20 phút rảnh
- [ ] Đã đọc README này

Sau khi chạy notebook:

- [ ] Đã xem lại bảng điều khiển chỉ số
- [ ] Đã tải xuống CSV export
- [ ] Đã kiểm tra giao diện chat
- [ ] Đã thử nghiệm với các tham số
- [ ] Đã lưu kết quả để tham khảo

---

## 📞 Liên Hệ

Đối với các vấn đề cụ thể về notebook này, tham khảo:
- `PROJECT_SUMMARY.txt` - Tổng quan dự án
- `Complete_Documentation.txt` - Tài liệu kỹ thuật đầy đủ
- `README.txt` - Hướng dẫn tham khảo nhanh

---

**Cập Nhật Lần Cuối**: 20 Tháng 8, 2026  
**Phiên Bản**: 2.0 (Đã xóa các cell API)  
**Số Cells**: 44 cells (20 bước)  
**Trạng Thái**: Sẵn Sàng Sản Xuất ✅

---

**Chúc Thử Nghiệm Vui Vẻ! 🚀**
