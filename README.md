# Chemical Safety Vector Knowledge Base

面向危险化学品安全标准与法规的领域向量知识库系统。

本项目完成了从原始 Excel 元数据、PDF 文档、OCR 解析、文本切分、向量化、FAISS 索引、Reranker 重排序，到 Streamlit Web 查询与文档增量上传的完整流程。

> 当前系统属于“向量知识库 + 检索重排序 + Web 管理界面”。  


---

## 1. 项目目标

危险化学品安全领域存在大量标准、法规、通知、管理办法和技术规范。这些文档通常以 PDF 形式保存，并存在以下问题：

- 文档数量多，人工查找效率低；
- 扫描版 PDF 缺少可复制文本；
- 标准编号、标题和文件名格式不统一；
- 传统关键词检索难以处理同义词和专业语义；
- 检索结果需要保留文档编号、标题、页码和原文依据；
- 新文档加入后需要自动补充知识库。

本项目的目标是构建一个可本地部署、可持续扩充、可溯源的危险化学品安全领域向量知识库。

---

## 2. 当前完成情况

### 2.1 数据规模

| 项目           | 当前数量 |
| -------------- | -------: |
| 文档主表记录   |      855 |
| 标准           |      615 |
| 法规           |      240 |
| 已匹配 PDF     |      854 |
| 未匹配文档     |        1 |
| 成功解析文档   |      854 |
| 文本 Chunk     |   16,491 |
| 向量维度       |    1,024 |
| FAISS 索引向量 |   16,491 |

文档匹配结果：

| 类型 | 总数 | 匹配数 | 匹配率 |
| ---- | ---: | -----: | -----: |
| 标准 |  615 |    615 | 100.0% |
| 法规 |  240 |    239 |  99.6% |
| 合计 |  855 |    854 |  99.9% |

唯一未匹配项为原始资料库中不存在对应 PDF 的法规文件。

### 2.2 已实现功能

- Excel 元数据清洗与标准化；
- 文档唯一 ID 生成；
- PDF 文件清单构建；
- 标准/法规元数据与 PDF 自动匹配；
- 文本型 PDF 解析；
- 扫描型 PDF 的 PaddleOCR GPU 识别；
- 文档级 JSON 结构化保存；
- 文本 Chunk 构建；
- BGE-M3 Embedding；
- FAISS 向量索引；
- BGE-Reranker-v2-m3 二阶段重排序；
- 命令行知识库检索；
- Streamlit Web 查询页面；
- PDF 上传页面；
- 新文档 OCR、Chunk、Embedding 和 FAISS 增量更新；
- 文档管理信息登记；
- 知识库状态展示。

---

## 3. 系统架构

```text
Excel Metadata
      │
      ▼
Document Master
      │
      ├───────────────┐
      │               │
      ▼               ▼
PDF Inventory     PDF Matching
      │               │
      └───────┬───────┘
              ▼
       PDF Parsing / OCR
              │
              ▼
      Structured Documents
              │
              ▼
         Text Chunking
              │
              ▼
       BGE-M3 Embedding
              │
              ▼
         FAISS Index
              │
              ▼
       Vector Retrieval
              │
              ▼
 BGE-Reranker-v2-m3
              │
              ▼
   Evidence-based Results
              │
              ▼
      Streamlit Web UI
```

新增文档的增量更新流程：

```text
Upload PDF
    │
    ▼
Save PDF
    │
    ▼
PaddleOCR Parsing
    │
    ▼
Chunk Builder
    │
    ▼
BGE-M3 Embedding
    │
    ▼
FAISS index.add()
    │
    ├──────────────► index_metadata.json
    │
    └──────────────► documents.json
```

---

## 4. 技术栈

### 4.1 开发语言与运行环境

| 技术                  | 用途                          |
| --------------------- | ----------------------------- |
| Python 3.12           | 项目主要开发语言              |
| Ubuntu 22.04          | 当前测试系统                  |
| CUDA 12.4             | GPU 推理环境                  |
| NVIDIA RTX 4090D 24GB | OCR、Embedding、Reranker 推理 |
| 60GB RAM              | 文档解析与批量处理            |

### 4.2 数据处理

| 技术         | 用途                         |
| ------------ | ---------------------------- |
| pandas       | Excel/CSV 数据清洗           |
| openpyxl     | 读取 Excel                   |
| pathlib      | 路径管理                     |
| JSON / JSONL | 文档、Chunk 和 Metadata 存储 |
| NumPy        | 向量矩阵处理                 |

### 4.3 PDF 与 OCR

| 技术                   | 用途               |
| ---------------------- | ------------------ |
| PyMuPDF / fitz         | PDF 页面读取与渲染 |
| PaddlePaddle-GPU 2.6.2 | OCR 推理框架       |
| PaddleOCR / PP-OCRv4   | 中文文档文字识别   |
| OpenCV                 | 图像处理           |
| Pillow                 | 图像文件处理       |

### 4.4 向量检索

| 技术                    | 用途                          |
| ----------------------- | ----------------------------- |
| BAAI/bge-m3             | 文本与查询向量化              |
| Sentence Transformers   | Embedding 模型加载与推理      |
| FAISS IndexFlatIP       | 归一化向量的精确内积检索      |
| BAAI/bge-reranker-v2-m3 | 对 FAISS 候选进行二阶段重排序 |
| Transformers            | Reranker 模型加载             |

### 4.5 Web 系统

| 技术                   | 用途                                          |
| ---------------------- | --------------------------------------------- |
| Streamlit              | Web 查询、上传、管理和状态页面                |
| Python Package Modules | 封装 Embedding、Retriever、Updater 等核心能力 |

---

## 5. 为什么使用这些方法

### 5.1 PaddleOCR

数据中存在大量扫描版 PDF，直接提取文本时可能只得到空字符串、水印或极少文本。因此采用 PaddleOCR 对 PDF 页面进行图像识别。

当前单个 7 页扫描标准的 OCR 测试耗时约数秒，854 份文档的批量解析已全部完成。

### 5.2 BGE-M3

BGE-M3 适合中文、多语言和较长文本的向量检索场景。当前每个 Chunk 被编码为 1,024 维归一化向量。

Embedding 输入由文档标题和正文组成：

```text
title
+
chunk text
```

这样可以同时利用文档主题和条款内容。

### 5.3 FAISS IndexFlatIP

Embedding 时使用：

```python
normalize_embeddings=True
```

向量归一化后，内积可用于表示余弦相似度。因此当前使用：

```python
faiss.IndexFlatIP(1024)
```

当前仅有 16,491 个向量，精确检索速度足够快，并且不会产生近似索引的召回损失。

### 5.4 BGE Reranker

FAISS 负责从全部 Chunk 中召回候选，Reranker 对查询和候选文本进行联合编码并重新排序。

当前检索流程：

```text
Query
  │
  ▼
BGE-M3
  │
  ▼
FAISS Top 50
  │
  ▼
BGE-Reranker-v2-m3
  │
  ▼
Final Top 5
```

二阶段架构可以降低仅依赖向量距离产生的误排序，并提升专业标准和法规条款的相关性。

---

## 6. 项目目录

```text
chemical_kb/
├── app/
│   ├── main.py
│   └── pages/
│       ├── 1_Query_Knowledge_Base.py
│       ├── 2_Upload_Document.py
│       ├── 3_Knowledge_Management.py
│       └── 4_System_Status.py
│
├── core/
│   ├── __init__.py
│   ├── config.py
│   ├── embedding.py
│   ├── vector_store.py
│   ├── reranker.py
│   ├── retriever.py
│   ├── parser.py
│   ├── chunker.py
│   ├── updater.py
│   └── document_manager.py
│
├── scripts/
│   ├── check_document_master.py
│   ├── build_pdf_inventory.py
│   ├── match_document_pdf.py
│   ├── 04_batch_parse_pdf_v2.py
│   ├── 05_build_chunks_v2.py
│   ├── 06_build_embedding.py
│   ├── 07_build_faiss_index.py
│   ├── init_document_manager.py
│   ├── query_vector_kb_answer_style.py
│   └── 09_test_reranker_retrieval.py
│
├── data/
│   ├── parsed/
│   │   └── document_master.csv
│   ├── pdf/
│   │   ├── 标准/
│   │   ├── 法规/
│   │   └── upload/
│   ├── parsed_documents/
│   ├── chunks/
│   │   └── chunks_v2.jsonl
│   ├── embeddings/
│   │   ├── chunks_embeddings.npy
│   │   └── chunks_metadata.json
│   ├── vector_store/
│   │   ├── faiss.index
│   │   └── index_metadata.json
│   └── knowledge/
│       └── documents.json
│
├── configs/
├── README.md
└── requirements.txt
```

实际文件名可能根据本地开发过程略有不同。运行前请确认 `core/config.py` 和各构建脚本中的输入、输出路径与本地目录一致。

---

## 7. 核心数据格式

### 7.1 文档主表

`data/parsed/document_master.csv`

主要字段：

| 字段           | 说明                         |
| -------------- | ---------------------------- |
| doc_id         | 文档唯一 ID                  |
| doc_type       | standard / regulation        |
| code           | 标准或法规编号               |
| title          | 文档标题                     |
| status         | ACTIVE / ABOLISHED / UNKNOWN |
| publish_date   | 发布日期                     |
| effective_date | 实施日期                     |
| issuer         | 发布机构                     |
| organization   | 归口单位                     |
| topic          | 主题分类                     |
| region         | 地区                         |
| level          | 文档级别                     |
| replacement    | 替代关系                     |
| source         | 数据来源                     |
| pdf_path       | PDF 文件路径                 |

### 7.2 Chunk Metadata

新增文档统一使用以下结构：

```json
{
  "chunk_id": "unique_chunk_id",
  "doc_id": "STD_AQ_3011_2007",
  "title": "连二亚硫酸钠包装安全要求",
  "document_type": "标准",
  "code": "AQ3011-2007",
  "source": "web_upload",
  "pdf_path": "/path/to/file.pdf",
  "page": 4,
  "text": "文档原文内容",
  "char_count": 800
}
```

### 7.3 文档管理数据

`data/knowledge/documents.json`

```json
[
  {
    "doc_id": "STD_AQ_3011_2007",
    "title": "连二亚硫酸钠包装安全要求",
    "document_type": "标准",
    "code": "AQ3011-2007",
    "source": "行业标准",
    "pdf_path": "/path/to/file.pdf",
    "pages": 7,
    "chunks": 8,
    "upload_time": "2026-08-04 10:00:00",
    "status": "active"
  }
]
```

---

## 8. 环境安装

### 8.1 创建环境

```bash
conda create -n kb python=3.12 -y
conda activate kb
```

### 8.2 建议依赖

```txt
torch>=2.6
torchvision
torchaudio

paddlepaddle-gpu==2.6.2
paddleocr==2.8.1

numpy==1.26.4
opencv-python==4.9.0.80
pymupdf
pillow

pandas
openpyxl
tqdm

sentence-transformers
transformers
accelerate
huggingface-hub
safetensors
sentencepiece
tokenizers

faiss-cpu
streamlit
pyyaml
python-dotenv
```

安装：

```bash
pip install -r requirements.txt
```

> FAISS 当前仅用于 16,491 个向量的 IndexFlatIP 检索，CPU 版本已经足够。Embedding 和 Reranker 使用 GPU。

### 8.3 PyTorch 注意事项

如果 BGE-M3 使用 `pytorch_model.bin` 权重，新版 Transformers 可能要求 PyTorch 2.6 或更高版本。

CUDA 12.4 示例：

```bash
pip install torch==2.6.0 torchvision torchaudio \
  --index-url https://download.pytorch.org/whl/cu124
```

检查：

```bash
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

---

## 9. 模型准备

模型未包含在 GitHub 仓库中，需要单独下载。

### 9.1 Embedding 模型

```text
BAAI/bge-m3
```

示例路径：

```text
/root/autodl-tmp/models/bge-m3
```

模型目录至少应包含：

```text
config.json
modules.json
config_sentence_transformers.json
sentence_bert_config.json
pytorch_model.bin 或 model.safetensors
tokenizer.json
tokenizer_config.json
special_tokens_map.json
sentencepiece.bpe.model
1_Pooling/config.json
```

### 9.2 Reranker 模型

```text
BAAI/bge-reranker-v2-m3
```

示例路径：

```text
/root/autodl-tmp/models/bge-reranker-v2-m3
```

模型目录至少应包含：

```text
config.json
model.safetensors
tokenizer.json
tokenizer_config.json
special_tokens_map.json
sentencepiece.bpe.model
```

### 9.3 配置模型路径

修改：

```text
core/config.py
```

示例：

```python
from pathlib import Path

BASE_DIR = Path("/root/autodl-tmp/chemical_kb")

VECTOR_INDEX = BASE_DIR / "data/vector_store/faiss.index"
VECTOR_METADATA = BASE_DIR / "data/vector_store/index_metadata.json"

EMBED_MODEL = "/root/autodl-tmp/models/bge-m3"
RERANK_MODEL = "/root/autodl-tmp/models/bge-reranker-v2-m3"

FAISS_TOP_K = 50
FINAL_TOP_K = 5
```

---

## 10. 首次构建知识库

以下流程仅在第一次构建、重新导入全部数据、修改 Chunk 策略或更换 Embedding 模型时运行。

### Step 1：检查文档主表

```bash
python scripts/check_document_master.py
```

检查：

- 文档总数；
- `doc_id` 是否重复；
- 标准和法规数量；
- 文档状态分布。

### Step 2：扫描 PDF

```bash
python scripts/build_pdf_inventory.py
```

输出：

```text
data/pdf_inventory.csv
```

### Step 3：匹配元数据与 PDF

```bash
python scripts/match_document_pdf.py
```

输出：

```text
data/document_pdf_mapping.csv
```

### Step 4：批量解析 PDF

```bash
python scripts/04_batch_parse_pdf_v2.py
```

输出：

```text
data/parsed_documents/
data/parse_report_v2.csv
```

当前项目已完成 854 个文档解析。

### Step 5：构建 Chunk

```bash
python scripts/05_build_chunks_v2.py
```

输出示例：

```text
data/chunks/chunks_v2.jsonl
```

当前生成 16,491 个 Chunk。

### Step 6：生成 Embedding

```bash
python scripts/06_build_embedding.py
```

输出：

```text
data/embeddings/chunks_embeddings.npy
data/embeddings/chunks_metadata.json
```

当前向量矩阵：

```text
(16491, 1024)
```

### Step 7：构建 FAISS 索引

```bash
python scripts/07_build_faiss_index.py
```

输出：

```text
data/vector_store/faiss.index
data/vector_store/index_metadata.json
```

### Step 8：初始化文档管理数据库

```bash
python scripts/init_document_manager.py
```

该脚本将历史文档同步到：

```text
data/knowledge/documents.json
```

运行前确认脚本中的 Chunk 文件路径正确。当前项目的 Chunk 文件通常为：

```text
data/chunks/chunks_v2.jsonl
```

如果脚本仍指向 `chunks.jsonl`，需要修改路径或使用自动搜索：

```python
chunk_files = list((BASE_DIR / "data/chunks").glob("*.jsonl"))
```

---

## 11. 日常运行流程

知识库已经构建完成后，不需要每次重新运行 OCR、Embedding 和 FAISS 构建脚本。

### 11.1 启动 Web 系统

进入项目根目录：

```bash
cd /root/autodl-tmp/chemical_kb
```

启动：

```bash
streamlit run app/main.py
```

AutoDL 环境中会显示类似地址：

```text
Local URL:    http://localhost:8501
Network URL:  http://172.17.0.3:8501
External URL: http://服务器公网IP:8501
```

浏览器访问 External URL 即可。

### 11.2 页面说明

#### 查询知识库

文件：

```text
app/pages/1_Query_Knowledge_Base.py
```

流程：

```text
输入问题
  │
  ▼
BGE-M3 查询向量
  │
  ▼
FAISS Top 50
  │
  ▼
BGE Reranker
  │
  ▼
显示 Top 5 文档依据
```

返回内容包括：

- 文档标题；
- 标准或法规编号；
- 文档类型；
- Reranker 分数；
- 原文内容；
- 页码信息。

#### 上传文档

文件：

```text
app/pages/2_Upload_Document.py
```

操作步骤：

1. 选择 PDF；
2. 填写文档标题；
3. 选择“标准”或“法规”；
4. 填写编号；
5. 填写来源；
6. 点击“加入知识库”。

系统执行：

```text
保存 PDF
→ OCR
→ Chunk
→ Embedding
→ FAISS 增量更新
→ Metadata 更新
→ documents.json 登记
```

新增完成后无需重新构建整个知识库。

#### 知识库管理

文件：

```text
app/pages/3_Knowledge_Management.py
```

当前支持：

- 查看文档数量；
- 查看有效文档数量；
- 查看 Chunk 总量；
- 按标题、编号和类型搜索；
- 查看文档详情；
- 删除 `documents.json` 中的管理记录。

> 当前版本的删除按钮只删除文档管理记录，尚未真正删除 FAISS 中的向量和 `index_metadata.json` 中的 Chunk。完整向量删除功能仍在开发中。

#### 系统状态

文件：

```text
app/pages/4_System_Status.py
```

展示：

- FAISS 向量数量；
- Metadata 数量；
- 向量维度；
- Embedding 模型；
- Reranker 模型；
- 系统状态。

---

## 12. 命令行查询

不启动网页时，可运行：

```bash
python scripts/query_vector_kb_answer_style.py
```

测试问题：

```text
保险粉包装有哪些安全要求？
```

```text
危险化学品重大危险源应该如何进行辨识和安全管理？
```

```text
液氯泄漏事故发生后应采取哪些应急处置措施？
```

---

## 13. 当前检索效果

已测试的典型问题能够召回预期文档：

| 查询问题                         | 主要召回结果                             |
| -------------------------------- | ---------------------------------------- |
| 保险粉包装有哪些安全要求？       | AQ3011-2007《连二亚硫酸钠包装安全要求》  |
| 危险化学品重大危险源安全管理要求 | 《危险化学品重大危险源监督管理暂行规定》 |
| 液氯使用安全要求有哪些？         | DB32/T 3617-2019《液氯使用安全技术规范》 |

系统不仅依赖标准编号或精确标题，也可以通过自然语言语义召回相关标准、法规和条款。

当前效果说明：

- BGE-M3 能够完成中文专业语义召回；
- FAISS 能够快速返回候选 Chunk；
- Reranker 能够将更直接回答问题的条款排到前面；
- Metadata 能够支持标题、编号、类型和原文溯源。

---

## 14. 什么时候需要重新构建知识库

### 不需要重新构建

以下操作只需启动 Web 系统：

- 查询已有知识；
- 查看系统状态；
- 查看文档列表；
- 通过上传页面添加少量新 PDF。

### 需要重新构建

以下情况需要重新执行部分或全部构建流程：

- 批量加入大量原始 PDF；
- 修改 Excel 文档主表；
- 修改 OCR 解析策略；
- 修改 Chunk 大小或重叠策略；
- 更换 Embedding 模型；
- 修改向量维度；
- FAISS 索引损坏；
- 需要从原始数据完全恢复知识库。

---

## 15. 当前限制

1. **尚未接入 LLM 生成层**  
   当前返回检索依据，不自动生成最终安全结论。

2. **FAISS 真正删除尚未完成**  
   当前管理页删除的是 `documents.json` 记录，FAISS 向量仍然存在。

3. **历史文档需要初始化管理数据库**  
   首次启用管理页前，需要运行 `init_document_manager.py`。

4. **上传页面默认使用 OCR**  
   对已有高质量文本层的 PDF，未来可优先直接提取文本，仅在质量不足时调用 OCR。

5. **当前主要面向单用户本地部署**  
   多用户并发上传可能引发 FAISS 和 JSON 文件同时写入冲突。

6. **Metadata 字段仍需进一步统一**  
   历史 Chunk 与网页上传 Chunk 的部分字段名称可能存在差异，例如 `page` 和 `page_start`。

7. **文件和模型较大**  
   PDF、模型、Embedding 和 FAISS 数据不建议直接提交 GitHub。

---

## 16. 后续计划

### 16.1 完整文档增删改查

- 将 FAISS 索引升级为支持显式 ID 的结构；
- 实现按 `doc_id` 删除全部向量；
- 同步删除 Chunk Metadata；
- 删除或归档原始 PDF；
- 支持重新解析和重新向量化。

### 16.2 统一 Metadata Schema

统一历史数据与新增数据：

```text
chunk_id
doc_id
title
document_type
code
status
source
pdf_path
page_start
page_end
text
char_count
```

### 16.3 增加解析质量检查

- 空页面检测；
- OCR 字符数检测；
- 页面异常检测；
- 低质量文档重新解析；
- 表格和章节结构识别。

### 16.4 RAG 问答

在当前检索结果上接入本地或在线 LLM：

```text
User Question
  → Retriever
  → Reranker
  → Top Evidence
  → LLM
  → Cited Answer
```

### 16.5 知识图谱

从标准和法规中抽取：

- 化学品；
- 设备；
- 危险源；
- 事故类型；
- 安全措施；
- 应急措施；
- 标准条款；
- 适用对象；
- 法规约束关系。

进一步研究 KG-enhanced RAG 或 GraphRAG。

### 16.6 API 服务

将核心能力封装为 FastAPI：

```text
POST /query
POST /upload
GET  /documents
DELETE /documents/{doc_id}
GET  /status
```

---

## 17. GitHub 上传建议

不建议提交：

- 原始 PDF；
- OCR 结果；
- 模型权重；
- Embedding 数组；
- FAISS 索引；
- 本地缓存；
- 用户上传文件。

建议 `.gitignore`：

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
.ipynb_checkpoints/

# Environments
.venv/
venv/
env/
.env

# Models
models/
*.bin
*.safetensors
*.pt
*.onnx

# Raw and generated data
data/pdf/
data/parsed_documents/
data/chunks/
data/embeddings/
data/vector_store/
data/knowledge/
data/*.csv
data/*.json
data/*.jsonl
data/*.npy

# Logs and temp files
*.log
*.tmp
*.png
*.jpg

# Streamlit
.streamlit/secrets.toml

# IDE
.vscode/
.idea/
```

建议保留少量脱敏示例数据：

```text
examples/
├── sample_document.json
├── sample_chunks.jsonl
└── sample_query_output.txt
```

---

## 18. 项目定位

当前项目不是一个简单的向量检索示例，而是一个面向危险化学品安全标准与法规的完整领域知识库工程，已经覆盖：

```text
数据治理
→ 文档匹配
→ OCR
→ 文本结构化
→ Chunk
→ Embedding
→ FAISS
→ Reranker
→ Web 查询
→ 增量上传
→ 文档管理
```

后续可在此基础上继续实现：

```text
Vector Knowledge Base
        +
LLM
        +
Knowledge Graph
        +
Agent
        =
Chemical Safety Intelligent Decision Support System
```

---

## 19. License

本项目当前用于科研学习、知识库构建实验和危险化学品安全领域技术验证。

原始标准、法规和 PDF 文档的版权及使用范围以其原始发布机构和数据来源要求为准。仓库不直接分发受版权保护的模型权重和原始文档。
