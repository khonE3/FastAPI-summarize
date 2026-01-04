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
├── 📂 app/                        # Backend Application
│   ├── __init__.py                # Package initializer
│   │
│   ├── 📂 api/                    # API Layer
│   │   ├── __init__.py
│   │   └── 📂 v1/                 # API Version 1
│   │       ├── __init__.py
│   │       ├── router.py          # Main router (รวม endpoints)
│   │       └── 📂 endpoints/      # API Endpoints
│   │           ├── __init__.py
│   │           ├── health.py      # Health check & status
│   │           └── summarize.py   # Summarization endpoints
│   │
│   ├── 📂 core/                   # Core Configuration
│   │   ├── __init__.py
│   │   └── config.py              # App settings & env variables
│   │
│   ├── 📂 models/                 # Data Models
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic request/response schemas
│   │
│   └── 📂 services/               # Business Logic
│       ├── __init__.py
│       └── summarizer.py          # AI summarization service (Singleton)
│
├── 📄 main.py                     # FastAPI application entry point
├── 🎨 frontend.py                 # Streamlit UI (Web Interface) ⭐
├── 🚀 run.py                      # Unified runner (Backend + Frontend)
│
├── 📦 pyproject.toml              # UV project config & dependencies
├── 🔒 uv.lock                     # Locked dependency versions
│
├── 📝 .env.example                # Environment variables template
├── 🚫 .gitignore                  # Git ignore rules
├── 🐍 .python-version             # Python version specification
│
└── 📖 README.md                   # Project documentation (this file)
```

### 📋 คำอธิบายไฟล์สำคัญ:

| ไฟล์ | หน้าที่ |
|------|--------|
| **main.py** | Entry point ของ FastAPI, กำหนด CORS, middleware, routing |
| **frontend.py** | Streamlit Web UI พร้อม custom CSS และ examples |
| **run.py** | สคริปต์รันทั้ง backend + frontend พร้อมกัน |
| **app/api/v1/router.py** | รวม API routes ทั้งหมด |
| **app/services/summarizer.py** | Singleton service โหลด BART model |
| **app/models/schemas.py** | Pydantic models สำหรับ validation |
| **app/core/config.py** | Settings และ environment configuration |
| **pyproject.toml** | UV dependencies และ project metadata |

---

## 🛠 เทคโนโลยีที่ใช้

| เทคโนโลยี | เวอร์ชัน | หน้าที่ |
|-----------|---------|--------|
| **FastAPI** | 0.128.0 | Modern Web Framework สำหรับสร้าง API |
| **Streamlit** | 1.52.2 | Frontend UI Framework (Web Interface) ⭐ |
| **Uvicorn** | 0.40.0 | ASGI Web Server (Production-ready) |
| **Pydantic** | 2.12.5 | Data Validation & Settings Management |
| **Transformers** | 4.57.3 | Hugging Face ML/NLP Library |
| **PyTorch** | 2.9.1 | Deep Learning Framework (Model Backend) |
| **UV** | Latest | Ultra-fast Python Package Manager (10-100x เร็วกว่า pip) |

### 📚 Dependencies เพิ่มเติม:
- **pydantic-settings** - Environment & Configuration management
- **python-multipart** - Form data & file uploads support
- **requests** - HTTP client สำหรับเชื่อมต่อ API
- **pandas** - Data manipulation (Streamlit dependency)
- **altair** - Data visualization (Streamlit charts)

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

### 4. รัน Application

#### ⚡ Quick Start (รัน Backend + Frontend พร้อมกัน)
```bash
# Windows
start.bat

# หรือใช้ Python
uv run python run.py
```

#### 🔧 รันแยกส่วน

**Backend เท่านั้น:**
```bash
# Windows
start_backend.bat

# หรือใช้ command line
uv run uvicorn main:app --reload
```
🌐 API: `http://localhost:8000`  
📚 Swagger UI: `http://localhost:8000/docs`

**Frontend เท่านั้น:**
```bash
# Windows
start_frontend.bat

# หรือใช้ command line
uv run streamlit run frontend.py
```
🎨 Streamlit UI: `http://localhost:8501`

---

## 📖 การใช้งาน

### 🎨 1. ใช้งานผ่าน Streamlit Frontend (แนะนำ)

1. รัน application: `uv run python run.py`
2. เปิดเบราว์เซอร์ที่ http://localhost:8501
3. วางข้อความที่ต้องการสรุป
4. ปรับความยาวตามต้องการ
5. กดปุ่ม "สรุปข้อความ"

**Features:**
- ✨ UI สวยงาม ใช้งานง่าย
- 📊 แสดงสถิติการสรุป
- 📚 มีตัวอย่างข้อความให้เลือก
- 🎯 ตรวจสอบสถานะ API อัตโนมัติ
- 📋 คัดลอกผลลัพธ์ได้

### 🔧 2. ใช้งานผ่าน API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 💻 3. ตัวอย่างการเรียก API

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

## 🎨 Screenshots

### Streamlit Frontend UI
```
┌────────────────────────────────────────────────┐
│  📝 AI Text Summarizer                         │
│  สรุปข้อความยาวๆ ให้สั้นและกระชับด้วย AI        │
├────────────────────────────────────────────────┤
│  Sidebar:        │  Main Content:              │
│  ⚙️ การตั้งค่า    │  📄 ข้อความต้นฉบับ           │
│  ✅ API Status   │  [Text Input Area]          │
│  📊 Settings     │                             │
│  - Max Length    │  ✨ ข้อความสรุป              │
│  - Min Length    │  [Summary Output]           │
│  📚 Examples     │  📊 สถิติ                   │
│                  │  - ความยาวต้นฉบับ            │
│                  │  - ความยาวสรุป              │
│                  │  - % บีบอัด                 │
└────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start Guide

### วิธีที่ 1: รันทั้งหมดพร้อมกัน (แนะนำ)
```bash
# Windows
start.bat

# หรือ
uv run python run.py
```

### วิธีที่ 2: รันแยกส่วน
```bash
# Terminal 1: Backend
uv run uvicorn main:app --reload

# Terminal 2: Frontend
uv run streamlit run frontend.py
```

### วิธีที่ 3: ใช้ API เท่านั้น
```bash
uv run uvicorn main:app --reload
# เข้าที่ http://localhost:8000/docs
```

---

## 💡 Tips & Tricks

1. **การสรุปครั้งแรกจะใช้เวลานาน** - โมเดลต้องดาวน์โหลดและโหลดเข้า memory (ประมาณ 1-2 นาที)
2. **ข้อความภาษาอังกฤษให้ผลลัพธ์ดีที่สุด** - โมเดล BART ถูกเทรนด้วยภาษาอังกฤษ
3. **ข้อความยาว = สรุปดีกว่า** - ข้อความควรยาวอย่างน้อย 100 คำเพื่อผลลัพธ์ที่ดี
4. **ปรับ max_length ตามความต้องการ** - ข้อความยาวควรใช้ max_length สูงกว่า

---

## 🐛 Troubleshooting

### ❌ API ไม่พร้อมใช้งาน
```bash
# ตรวจสอบว่า backend รันอยู่หรือไม่
curl http://localhost:8000/api/v1/health

# ถ้าไม่รัน ให้เริ่มใหม่
uv run uvicorn main:app --reload
```

### ⏱️ Timeout เมื่อสรุปครั้งแรก
- ปกติ - โมเดลกำลังโหลด
- รอ 1-2 นาที แล้วลองใหม่

### 💾 Model ดาวน์โหลดช้า
- โมเดล BART มีขนาดประมาณ 1.6 GB
- ครั้งแรกจะดาวน์โหลดและ cache ไว้

---

## 📄 License

MIT License

---

## 👨‍💻 Author
, Streamlit,
Created with ❤️ using FastAPI and UV
