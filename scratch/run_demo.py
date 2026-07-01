"""
scratch/run_demo.py
───────────────────
Full demo verification script.
Sets up local mock db entries, generates a sample PDF on disk, extracts and
indexes its text into ChromaDB, and runs a RAG query loop.
"""

import sys
import os
import uuid
from pathlib import Path

# Add backend directory to python path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.append(str(backend_path))

# Setup environment variables for demo if not already loaded
os.environ.setdefault("SECRET_KEY", "demo_secret_key_for_hackathon_testing_purposes")
os.environ.setdefault("DATABASE_URL", "sqlite:///./demo_patients.db")
os.environ.setdefault("UPLOAD_DIR", "demo_uploads")
os.environ.setdefault("CHROMA_DB_PATH", "demo_chroma_db")

from sqlalchemy.orm import Session
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.user import User
from app.models.patient import Patient
from app.models.report import Report
from app.core.security import hash_password
from app.utils.pdf_extractor import extract_text_from_pdf
from app.utils.file_handler import ALLOWED_MIME_TYPES
from app.rag.rag_pipeline import index_report, answer_question

# We use standard report structure
MOCK_REPORT_CONTENT = """
PATIENT MEDICAL ASSESSMENT REPORT
─────────────────────────────────
NAME: John Doe
AGE: 45
BLOOD GROUP: O-Pos

VITAL SIGNS:
• BP: 142/95 mmHg (Elevated)
• Heart Rate: 78 bpm
• Temp: 98.6 F

CLINICAL SUMMATION & DIAGNOSIS:
Patient presents with symptoms consistent with Stage 1 Hypertension and chronic fatigue.
Primary diagnosis: Moderate Hypertension, Mild Hyperlipidemia.

ALLERGIES:
• Severe allergy to Penicillin (causes anaphylaxis).
• Mild allergy to Sulfa-based medications (causes rash).

CURRENT TREATMENT PLAN / MEDICATIONS:
1. Hydrochlorothiazide 12.5 mg tablet - Take 1 tablet by mouth daily in the morning.
2. Atorvastatin 20 mg tablet - Take 1 tablet by mouth daily at bedtime.
3. Restrict dietary sodium intake to under 2,000 mg per day.
4. Regular moderate cardiovascular exercise for 30 minutes, 5 days per week.

FOLLOW UP:
Return to clinic in 4 weeks for repeat blood pressure check and lipid panel.
"""

def create_fake_pdf(output_path: Path):
    """
    Generate a simple plain-text-based PDF file.
    Since we can't compile a complex binary PDF writer easily, we will write a clean
    textual PDF format that PyPDF2/pdfminer.six can read.
    """
    # Create directory if missing
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # We output a simple PDF structure that PyPDF2 can parse as text pages
    pdf_content = (
        "%PDF-1.4\n"
        "1 0 obj <</Type /Catalog /Pages 2 0 R>> endobj\n"
        "2 0 obj <</Type /Pages /Kids [3 0 R] /Count 1>> endobj\n"
        "3 0 obj <</Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources <</Font <</F1 5 0 R>>>>>> endobj\n"
        "4 0 obj\n"
        f"<</Length {len(MOCK_REPORT_CONTENT)}>>\n"
        "stream\n"
        "BT\n"
        "/F1 12 Tf\n"
        "72 712 Td\n"
    )
    
    # Clean PDF stream wrapping lines
    lines = MOCK_REPORT_CONTENT.strip().split("\n")
    for line in lines:
        # Escape parenthesis
        escaped = line.replace("(", "\\(").replace(")", "\\)")
        pdf_content += f"({escaped}) Tj T*\n"
        
    pdf_content += (
        "ET\n"
        "endstream\n"
        "endobj\n"
        "5 0 obj <</Type /Font /Subtype /Type1 /BaseFont /Helvetica>> endobj\n"
        "xref\n"
        "0 6\n"
        "0000000000 65535 f\n"
        "trailer <</Size 6 /Root 1 0 R>>\n"
        "startxref\n"
        "0\n"
        "%%EOF\n"
    )
    
    output_path.write_bytes(pdf_content.encode("latin1", errors="ignore"))
    print(f"Generated mock PDF file: {output_path}")

def run_demo():
    print("==================================================")
    print("      CHRONIC PATIENT MEMORY SYSTEM DEMO          ")
    print("==================================================")
    
    # 1. Initialize DB
    print("\n[1/5] Initializing Database...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    # 2. Seed Doctor
    print("\n[2/5] Seeding Doctor details...")
    doctor = db.query(User).filter(User.email == "demo_doctor@hospital.com").first()
    if not doctor:
        doctor = User(
            name="Dr. Demo Specialist",
            email="demo_doctor@hospital.com",
            hashed_password=hash_password("Demo@12345"),
            is_active=True
        )
        db.add(doctor)
        db.commit()
        db.refresh(doctor)
    print(f"Active Doctor: {doctor.name} ({doctor.email})")
    
    # 3. Create Patient
    print("\n[3/5] Creating patient record...")
    patient = db.query(Patient).filter(Patient.name == "John Doe", Patient.doctor_id == doctor.id).first()
    if not patient:
        patient = Patient(
            doctor_id=doctor.id,
            name="John Doe",
            age=45,
            gender="Male",
            blood_group="O-",
            chronic_conditions="Hypertension, Mild Hyperlipidemia",
            current_medications="Hydrochlorothiazide 12.5mg, Atorvastatin 20mg",
            allergies="Penicillin (Anaphylaxis), Sulfa (Rash)"
        )
        db.add(patient)
        db.commit()
        db.refresh(patient)
    print(f"Created Patient: {patient.name}, Age {patient.age}, ID: {patient.id}")

    # 4. Generate Mock PDF & Index it
    print("\n[4/5] Simulating Medical Report Upload...")
    pdf_filename = f"{uuid.uuid4().hex}_john_doe_blood_pressure.pdf"
    uploads_dir = Path("demo_uploads") / str(patient.id)
    pdf_path = uploads_dir / pdf_filename
    
    create_fake_pdf(pdf_path)
    
    # Read/extract text (Simulating the backend pipeline)
    text = extract_text_from_pdf(pdf_path)
    
    report = db.query(Report).filter(Report.original_filename == "john_doe_blood_pressure.pdf", Report.patient_id == patient.id).first()
    if not report:
        report = Report(
            patient_id=patient.id,
            filename=pdf_filename,
            original_filename="john_doe_blood_pressure.pdf",
            file_path=str(pdf_path),
            file_size=pdf_path.stat().st_size,
            extracted_text=text,
            report_type="Lab Report",
            description="Mock diagnostics blood pressure assessment for John Doe",
            is_embedded=False
        )
        db.add(report)
        db.commit()
        db.refresh(report)

    # Trigger indexing
    chunks_count = index_report(
        patient_id=patient.id,
        report_id=report.id,
        extracted_text=text
    )
    if chunks_count > 0:
        report.is_embedded = True
        db.commit()
        db.refresh(report)
        print(f"Successfully indexed report! Stored {chunks_count} chunks inside ChromaDB.")
    else:
        print("Warning: Indexing yielded 0 chunks.")

    # 5. Run Chatbot Q&A simulation
    print("\n[5/5] Running Chatbot Queries...")
    from app.core.config import settings
    
    queries = [
        "What are the patient's blood pressure levels?",
        "What is John Doe allergic to?",
        "Is the patient taking any cholesterol medications?",
        "What is the patient's favorite restaurant?" # Test fallback
    ]
    
    has_api_key = settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "REPLACE_WITH_YOUR_GEMINI_API_KEY"
    
    for q in queries:
        print("\n" + "─"*50)
        print(f"QUESTION: {q}")
        print("─"*50)
        answer, sources = answer_question(patient.id, patient.name, q)
        print(f"RETRIEVED SOURCE CHUNKS ({len(sources)}):")
        for s in sources[:1]:
            print(f"  > {s[:160]}...")
        print(f"\nAI ANSWER:\n{answer}")
        
    print("\n" + "="*50)
    print("Demo execution finished. Local databases loaded at './demo_patients.db'.")
    print("==================================================")
    db.close()

if __name__ == "__main__":
    run_demo()
