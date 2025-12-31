# 📝 FastAPI Summarize

API สำหรับสรุปข้อความด้วย AI (Text Summarization) พัฒนาด้วย FastAPI และ Hugging Face Transformers

## 📋 สารบัญ

- [คอนเซปของโปรเจค](#-คอนเซปของโปรเจค)
- [โครงสร้างโปรเจค](#-โครงสร้างโปรเจค)
- [เทคโนโลยีที่ใช้](#-เทคโนโลยีที่ใช้)
- [การติดตั้ง](#-การติดตั้ง)
- [การใช้งาน](#-การใช้งาน)
- [API Endpoints](#-api-endpoints)

---

## 🎯 คอนเซปของโปรเจค

### 1. **FastAPI Framework**
FastAPI เป็น Web Framework สำหรับ Python ที่มีคุณสมบัติเด่น:
- **Fast**: ประสิทธิภาพสูง เทียบเท่า NodeJS และ Go
- **Fast to code**: เขียนโค้ดเร็ว ลดเวลาพัฒนา 200-300%
- **Type hints**: ใช้ Python type hints ช่วยตรวจจับ errors
- **Auto documentation**: สร้าง Swagger UI และ ReDoc อัตโนมัติ
- **Async support**: รองรับ async/await ทำให้รองรับ concurrent requests ได้ดี

### 2. **Project Structure Pattern**
โปรเจคใช้ **Layered Architecture** แบ่งโครงสร้างตามหน้าที่:

```
app/
├── api/          # API Layer - จัดการ HTTP requests/responses
├── core/         # Core Layer - Configuration, Settings
├── models/       # Models Layer - Pydantic schemas
└── services/     # Service Layer - Business logic
```

### 3. **Dependency Injection**
FastAPI รองรับ Dependency Injection ที่ช่วยให้:
- จัดการ dependencies ได้ง่าย
- ทดสอบ (Testing) ได้สะดวก
- โค้ดมี reusability สูง

### 4. **Pydantic Models**
ใช้ Pydantic สำหรับ:
- **Data Validation**: ตรวจสอบข้อมูลอัตโนมัติ
- **Serialization**: แปลง Python objects เป็น JSON
- **Documentation**: สร้าง JSON Schema สำหรับ API docs

### 5. **Singleton Pattern**
Service class ใช้ Singleton Pattern เพื่อ:
- โหลด ML model เพียงครั้งเดียว
- ประหยัด memory
- เพิ่มประสิทธิภาพการทำงาน

### 6. **Text Summarization with Transformers**
ใช้ Hugging Face Transformers library:
- Model: `facebook/bart-large-cnn` (state-of-the-art summarization)
- Pipeline: ใช้ pipeline abstraction สำหรับความง่าย
- Supports: ปรับ max/min length ได้ตามต้องการ

---

## 📁 โครงสร้างโปรเจค

```
FastAPI-summarize/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py           # รวม routes ทั้งหมด
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── health.py       # Health check endpoints
│   │           └── summarize.py    # Summarization endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Application configuration
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic schemas
│   └── services/
│       ├── __init__.py
│       └── summarizer.py          # Summarization service
├── main.py                        # Application entry point
├── pyproject.toml                 # Project dependencies (UV)
├── uv.lock                        # Lock file
├── .env.example                   # Environment variables example
├── .gitignore
└── README.md
```

---

## 🛠 เทคโนโลยีที่ใช้

| เทคโนโลยี | หน้าที่ |
|-----------|--------|
| **FastAPI** | Web Framework |
| **Uvicorn** | ASGI Server |
| **Pydantic** | Data Validation & Settings |
| **Transformers** | ML/NLP Library (Hugging Face) |
| **PyTorch** | Deep Learning Backend |
| **UV** | Package Manager (เร็วกว่า pip 10-100x) |

---

## 🚀 การติดตั้ง

### Prerequisites
- Python 3.11+
- UV package manager

### 1. Clone repository
```bash
git clone <repository-url>
cd FastAPI-summarize
```

### 2. ติดตั้ง dependencies ด้วย UV
```bash
# ติดตั้ง UV (ถ้ายังไม่มี)
pip install uv

# ติดตั้ง dependencies
uv sync
```

### 3. สร้างไฟล์ .env (optional)
```bash
cp .env.example .env
```

### 4. รัน Server
```bash
# Development mode
uv run uvicorn main:app --reload

# หรือ
uv run python main.py
```

Server จะเริ่มทำงานที่ `http://localhost:8000`

---

## 📖 การใช้งาน

### เข้าถึง API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### ตัวอย่างการเรียก API

#### สรุปข้อความ
```bash
curl -X POST "http://localhost:8000/api/v1/summarize/" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python based on standard Python type hints. The key features are: Fast, Fast to code, Fewer bugs, Intuitive, Easy, Short, Robust, Standards-based.",
    "max_length": 100,
    "min_length": 30
  }'
```

#### ตรวจสอบสถานะ API
```bash
curl http://localhost:8000/api/v1/health
```

---

## 🔗 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Root endpoint |
| `GET` | `/api/v1/health` | ตรวจสอบสถานะ API |
| `POST` | `/api/v1/summarize/` | สรุปข้อความ |
| `POST` | `/api/v1/summarize/batch` | สรุปข้อความหลายรายการ |

---

## 📝 Request/Response Schemas

### SummarizeRequest
```json
{
  "text": "string (required, min 10 chars)",
  "max_length": "integer (optional, default: 150)",
  "min_length": "integer (optional, default: 30)"
}
```

### SummarizeResponse
```json
{
  "original_text": "string",
  "summary": "string",
  "original_length": "integer",
  "summary_length": "integer",
  "compression_ratio": "float"
}
```

---

## ⚙️ Configuration

ตั้งค่าผ่าน Environment Variables หรือไฟล์ `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | FastAPI Summarize | ชื่อ Application |
| `DEBUG` | True | Debug mode |
| `MODEL_NAME` | facebook/bart-large-cnn | Summarization model |
| `MAX_INPUT_LENGTH` | 1024 | ความยาวสูงสุดของ input |

---

## 🏗 Architecture Concepts

### Layered Architecture
```
┌─────────────────────────────────────┐
│           API Layer                 │  ← HTTP Request/Response
│    (endpoints/summarize.py)         │
├─────────────────────────────────────┤
│         Service Layer               │  ← Business Logic
│    (services/summarizer.py)         │
├─────────────────────────────────────┤
│          Model Layer                │  ← Data Validation
│     (models/schemas.py)             │
├─────────────────────────────────────┤
│          Core Layer                 │  ← Configuration
│      (core/config.py)               │
└─────────────────────────────────────┘
```

### Request Flow
```
Client Request
      ↓
   FastAPI
      ↓
   Router (api/v1/router.py)
      ↓
   Endpoint (endpoints/summarize.py)
      ↓
   Pydantic Validation (models/schemas.py)
      ↓
   Service (services/summarizer.py)
      ↓
   ML Model (Transformers)
      ↓
   Response to Client
```

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Created with ❤️ using FastAPI and UV
