# Chronic Patient Memory System (CPMS) 🩺🧠
An AI-powered Retrieval-Augmented Generation (RAG) assistant that helps doctors query patient histories, laboratory reports, and clinical notes in real-time. Designed and built for the **Hangover Hackathon**.

---

## ⚡ Quick Hackathon Pitch

- **The Problem**: Doctors spend up to **33% of their workday** scrolling through unstructured medical history, discharge summaries, and PDFs to piece together a patient's history. During critical cases, delays cost lives.
- **The Solution**: **CPMS** utilizes multi-tenant local vector indexing (ChromaDB) to partition data by patient. It processes uploads instantly, indexes raw data using Sentence Transformers (`all-MiniLM-L6-v2`), and lets doctors consult the patient's record through a secure chatbot interface powered by the **Gemini 1.5 Flash API**.
- **The Key Innovator (Anti-Hallucination Guard)**: The AI chatbot is structurally confined. If the query parameters fall outside the patient's records, it defaults to:  
  `"I couldn't find that information in the patient's medical history."`
- **Architecture**: Separated modular FastAPI Backend + React Vite Glassmorphism Frontend. Designed to scale seamlessly from SQLite to PostgreSQL.

---

## 📂 Repository Structure

```
chronic-patient-memory-system/
├── backend/                        # FastAPI App
│   ├── main.py                     # Entry point
│   ├── requirements.txt            # Python dependencies
│   ├── alembic.ini                 # DB migrations configuration
│   ├── .env.example                # Configuration blueprint
│   └── app/
│       ├── api/v1/endpoints/       # Router controllers (Auth, Patients, Reports, Chat)
│       ├── core/                   # Security, dependencies, and settings
│       ├── db/                     # DB engine, schemas, seeds
│       ├── models/                 # SQLAlchemy models
│       ├── schemas/                # Pydantic schemas (Request/Response validators)
│       ├── services/               # Scoped business rules
│       ├── rag/                    # AI core (Embeddings, ChromaDB interface, Gemini client)
│       └── utils/                  # PDF extractors, validation helpers
│
├── frontend/                       # React App
│   ├── package.json                # npm dependencies
│   ├── vite.config.js              # Dev proxy configuration
│   ├── vercel.json                 # Vercel hosting rules
│   ├── index.html                  # HTML entry with SEO metadata
│   └── src/
│       ├── api/                    # Axios instances
│       ├── components/             # Reusable UI widgets
│       ├── hooks/                  # Custom async hooks
│       ├── pages/                  # Route views
│       ├── store/                  # Zustand state storage
│       └── styles/                 # global.css design tokens
│
├── docs/                           # Manual docs
│   ├── API.md                      # Complete endpoint schema specifications
│   └── DEPLOYMENT.md               # DevOps staging checklist
│
├── render.yaml                     # Render Blueprint deploy file
├── .gitignore                      # Git exclusion rules
└── scratch/                        # Sandbox test utilities
    ├── test_rag.py                 # RAG pipeline test harness
    └── run_demo.py                 # Interactive test seed script
```

---

## 🚀 Running CPMS Locally

### 1. Prerequisite Checks
Ensure you have **Python 3.10+** and **Node.js 18+** installed.

### 2. Backend Installation & Startup
```bash
# Navigate to the backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # macOS / Linux

# Install libraries
pip install -r requirements.txt

# Create environment configuration
copy .env.example .env     # Windows
cp .env.example .env       # macOS / Linux

# Edit .env and supply your GEMINI_API_KEY. Set a strong SECRET_KEY.
```

Start the application:
```bash
uvicorn main:app --reload --port 8000
```
- **Swagger Documentation**: http://localhost:8000/docs
- **Mock Administrator Login**: `admin@hospital.com` / `Admin@12345`

### 3. Frontend Installation & Startup
```bash
# Navigate to the frontend directory
cd ../frontend

# Install dependencies
npm install

# Run Vite dev server
npm run dev
```
Open your browser at **http://localhost:5173** to preview the dashboard.

---

## 🧪 Testing the RAG Pipeline (Without Frontend UI)

You can run the simulated RAG run loop right in your shell. The demo script creates a mock database locally, structures a dummy multi-page clinical report on disk, indexes its content into ChromaDB, and runs natural language queries.

```bash
# Make sure your virtual env is active in the backend directory
cd chronic-patient-memory-system
python scratch/run_demo.py
```

---

## 🛸 Production Deployment Blueprints

### Render.com Deploy (FastAPI + Storage)
The codebase includes a root-level `render.yaml` configuration.  
When deploying to Render, link your GitHub repository and select **Blueprint**. This automatically mounts a **1GB Persistent Disk** to hold SQLite database entries, uploaded PDFs, and vector index databases without wiping files during builds.

### Vercel Deploy (React)
The frontend folder includes a `vercel.json` rewrite file. This ensures all routes rewrite back to `index.html` to support client-side React routing, and proxies `/api` endpoints straight to your production backend.

---

## 🏆 Hackathon Presentation Checklist

When showcasing the system to judges, highlight these design patterns:
1. **Zero-Trust Multi-Tenancy**: ChromaDB handles context segmentation by generating an isolated vector storage collection for each patient ID. Doctors cannot accidentally access another patient's data.
2. **Context-Confined Prompts (Anti-Hallucination)**: System prompt weights prevent Gemini from referencing its broad training data for medical queries, enforcing strict grounding inside the indexed PDF files.
3. **Database Portability**: The SQLAlchemy session relies on pragmas that speed up SQLite reads (WAL logging). It is built to migrate to PostgreSQL with a single-line config modification inside `.env`.
4. **Resilient Offline PDF Parser**: Utilizes a fallback extraction matrix. If quick PDF scanners fail to extract text, it rolls over to a structural positional OCR framework.
