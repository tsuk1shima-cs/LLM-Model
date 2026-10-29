# Tổng Hợp Kết Quả Thực Nghiệm LLM Theo `EXPERIMENT_PLAN_VI`

- **Run Session ID:** `run_20261026T231603Z_a3b74f`
- **Thời gian tạo (UTC):** `2026-10-27T00:47:22.701326+00:00`
- **GPU / VRAM:** `Tesla T4 (15360.0 MB)`
- **Chế độ dữ liệu E3:** `LOCKED_CUSTOM_HUIT_RAGBENCH`

## Bảng 1 — Runtime & Model Manifest (E0)

| Model (Paper)                               | Ollama Tag                    | Digest (12 chars)   | Quantization   |   Effective Context | Thinking Mode                   | VRAM Offload (MB / %)   |
|:--------------------------------------------|:------------------------------|:--------------------|:---------------|--------------------:|:--------------------------------|:------------------------|
| Qwen/Qwen3.5-4B (Report Baseline)           | qwen3.5:4b                    | d8b0f5e9760cd168203 | Q4_K_M         |                8192 | disabled_via_ollama_think_false | 3209.0 MB (100.0%)      |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | qwen3:4b-instruct-2507-q4_K_M | 0edcdef34593eac1aa2 | Q4_K_M         |                8192 | disabled_via_ollama_think_false | 3697.9 MB (100.0%)      |

## Bảng 4 — HUIT Grounded QA & Refusal: 2 LLM × 4 RAG Contexts (E3)

> **Ghi chú phương pháp (Mục 6.E3):** Các cột Correctness / Evidence Support / Temporal Validity chính thức trên bài báo sử dụng kết quả chấm mù của 2 Annotator độc lập từ file `annotations/e3_blind_annotation_sheet.csv` (không dùng LLM-as-judge).

| Model                                       | RAG Context          |   Answered Rate (%) | Citation P (%)       | Citation R (%)    | Citation F1 (%)   | Refusal P / R / F1 (%)   |   Exact Refusal Format (%) |   Aux Token-F1 (Dev Only) | TTFT p50 / p95 (ms)   | Latency p50 / p95 (ms)   |   Tok/s (mean) |   Peak VRAM (MB) |   Failure Rate (%) |
|:--------------------------------------------|:---------------------|--------------------:|:---------------------|:------------------|:------------------|:-------------------------|---------------------------:|--------------------------:|:----------------------|:-------------------------|---------------:|-----------------:|-------------------:|
| Qwen/Qwen3.5-4B (Report Baseline)           | no_rag               |                 0.7 | 0.0 [0.0, 0.0]       | 0.0 [0.0, 0.0]    | 0.0 [0.0, 0.0]    | 33.5 / 100.0 / 50.2      |                      100   |                       0.2 | 200 / 236             | 482 / 634                |           30.7 |             4013 |                  0 |
| Qwen/Qwen3.5-4B (Report Baseline)           | best_dense           |               100   | 100.0 [100.0, 100.0] | 83.0 [80.3, 85.7] | 88.7 [86.9, 90.4] | 100.0 / 84.7 / 91.7      |                       99.2 |                      48.6 | 724 / 1121            | 1875 / 3809              |           29.2 |             4013 |                  0 |
| Qwen/Qwen3.5-4B (Report Baseline)           | best_hybrid          |               100   | 100.0 [100.0, 100.0] | 84.7 [82.0, 87.3] | 89.8 [88.0, 91.6] | 100.0 / 85.3 / 92.1      |                       98.4 |                      48.1 | 721 / 1108            | 1936 / 3538              |           29.4 |             4013 |                  0 |
| Qwen/Qwen3.5-4B (Report Baseline)           | best_hybrid_reranker |               100   | 100.0 [100.0, 100.0] | 86.3 [83.7, 88.8] | 90.9 [89.1, 92.6] | 100.0 / 84.7 / 91.7      |                       99.2 |                      47.6 | 559 / 994             | 1710 / 3677              |           31.2 |             4013 |                  0 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | no_rag               |                 0.3 | 0.0 [0.0, 0.0]       | 0.0 [0.0, 0.0]    | 0.0 [0.0, 0.0]    | 33.4 / 100.0 / 50.1      |                       99.6 |                       0.1 | 48 / 56               | 294 / 303                |           54.4 |             3845 |                  0 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_dense           |                96.7 | 81.7 [77.5, 85.7]    | 71.3 [67.3, 75.2] | 74.2 [70.3, 77.9] | 93.4 / 94.0 / 93.7       |                      100   |                      48.7 | 314 / 865             | 1135 / 3170              |           39.3 |             3845 |                  0 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_hybrid          |               100   | 86.7 [83.2, 90.2]    | 74.7 [70.7, 78.3] | 78.1 [74.7, 81.3] | 100.0 / 94.0 / 96.9      |                      100   |                      50.3 | 304 / 780             | 1308 / 2855              |           40.7 |             3845 |                  0 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_hybrid_reranker |               100   | 93.0 [90.0, 95.7]    | 77.7 [74.0, 81.2] | 82.8 [79.4, 85.7] | 100.0 / 94.0 / 96.9      |                      100   |                      49.9 | 234 / 524             | 1126 / 2777              |           43   |             3845 |                  0 |

## Bảng 4b — Phân Tích Theo 3 Mức Khó (Single-hop / Multi-section / Temporal-procedural)

| Model                                       | RAG Context          | Difficulty          |   N |   Citation F1 (%) |   Aux Token-F1 |
|:--------------------------------------------|:---------------------|:--------------------|----:|------------------:|---------------:|
| Qwen/Qwen3.5-4B (Report Baseline)           | best_hybrid          | single_hop          |  96 |             100   |           47.3 |
| Qwen/Qwen3.5-4B (Report Baseline)           | best_hybrid          | multi_section       | 104 |              83.3 |           44.9 |
| Qwen/Qwen3.5-4B (Report Baseline)           | best_hybrid          | temporal_procedural | 100 |              86.7 |           52.3 |
| Qwen/Qwen3.5-4B (Report Baseline)           | best_hybrid_reranker | single_hop          |  96 |             100   |           46.4 |
| Qwen/Qwen3.5-4B (Report Baseline)           | best_hybrid_reranker | multi_section       | 104 |              83.3 |           46.1 |
| Qwen/Qwen3.5-4B (Report Baseline)           | best_hybrid_reranker | temporal_procedural | 100 |              90   |           50.3 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_hybrid          | single_hop          |  96 |              89.6 |           53.8 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_hybrid          | multi_section       | 104 |              64.1 |           47.5 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_hybrid          | temporal_procedural | 100 |              81.7 |           49.8 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_hybrid_reranker | single_hop          |  96 |              99   |           53.8 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_hybrid_reranker | multi_section       | 104 |              73.7 |           47.8 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_hybrid_reranker | temporal_procedural | 100 |              76.7 |           48.2 |

## Bảng 5 — VMLU Zero-Shot Tiếng Việt Ngoài Miền HUIT (E4)

| Model                                       | Eval Split (Labeled)   | Overall Acc (% [95% CI])   |   Macro 58 Subjects (%) |   Macro 4 Domains (%) |   STEM (%) |   Social Science (%) |   Humanity (%) |   Other (%) |   Parse Failure (%) | Latency p50/p95 (ms)   |
|:--------------------------------------------|:-----------------------|:---------------------------|------------------------:|----------------------:|-----------:|---------------------:|---------------:|------------:|--------------------:|:-----------------------|
| Qwen/Qwen3.5-4B (Report Baseline)           | VMLU valid (n=744)     | 62.90 [59.27, 66.26]       |                   62.15 |                 60.76 |      68.12 |                62.24 |          59.76 |       52.93 |                   0 | 241 / 291              |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | VMLU valid (n=744)     | 63.44 [59.54, 66.80]       |                   62.56 |                 61.04 |      71.43 |                62.2  |          56.86 |       53.66 |                   0 | 91 / 133               |

## Bảng 8 (Phần LLM/RAG) — Error Taxonomy

| Model                                       | RAG Context          |   Retrieval Miss |   Outdated Doc Cited |   Unsupported / No Gold Cit |   Hallucinated Chunk ID |   False Refusal (on Answerable) |   Missed Refusal (on Unanswerable) |   Runtime Timeout/Error |
|:--------------------------------------------|:---------------------|-----------------:|---------------------:|----------------------------:|------------------------:|--------------------------------:|-----------------------------------:|------------------------:|
| Qwen/Qwen3.5-4B (Report Baseline)           | no_rag               |                0 |                    0 |                           2 |                       0 |                             298 |                                  0 |                       0 |
| Qwen/Qwen3.5-4B (Report Baseline)           | best_dense           |                0 |                    0 |                           0 |                       0 |                               0 |                                 23 |                       0 |
| Qwen/Qwen3.5-4B (Report Baseline)           | best_hybrid          |                0 |                    0 |                           0 |                       0 |                               0 |                                 22 |                       0 |
| Qwen/Qwen3.5-4B (Report Baseline)           | best_hybrid_reranker |                0 |                   10 |                           0 |                       0 |                               0 |                                 23 |                       0 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | no_rag               |                0 |                    0 |                           1 |                       0 |                             299 |                                  0 |                       0 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_dense           |                0 |                   10 |                          35 |                      35 |                              10 |                                  9 |                       0 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_hybrid          |                0 |                   10 |                          30 |                      30 |                               0 |                                  9 |                       0 |
| Qwen/Qwen3-4B-Instruct-2507 (Supplementary) | best_hybrid_reranker |                0 |                    0 |                          21 |                      11 |                               0 |                                  9 |                       0 |
