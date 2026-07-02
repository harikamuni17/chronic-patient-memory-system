"""
Seed a small CPMS demo dataset for local judging/demo flows.

Run from backend:
    python -m app.db.seed_demo
"""

from __future__ import annotations

from app.core.security import hash_password
from app.db.base import Base  # noqa: F401 - registers all ORM relationships
from app.db.init_db import create_tables
from app.db.session import SessionLocal
from app.models.chat import ChatMessage, ChatSession
from app.models.patient import Patient
from app.models.report import Report
from app.models.user import User

DEMO_EMAIL = "demo.doctor@cpms.local"
DEMO_PASSWORD = "Demo@12345"
ADMIN_EMAIL = "admin@hospital.com"
ADMIN_PASSWORD = "Admin@12345"


def seed_demo_data(
    email: str = DEMO_EMAIL,
    password: str = DEMO_PASSWORD,
    name: str = "Dr. Demo Clinician",
) -> dict[str, int | str]:
    create_tables()
    db = SessionLocal()
    try:
        doctor = db.query(User).filter(User.email == email).first()
        if not doctor:
            doctor = User(
                name=name,
                email=email,
                hashed_password=hash_password(password),
                is_active=True,
            )
            db.add(doctor)
            db.flush()

        existing_demo_patient = (
            db.query(Patient)
            .filter(Patient.doctor_id == doctor.id, Patient.name == "Ananya Rao")
            .first()
        )
        if existing_demo_patient:
            return {
                "doctor_id": doctor.id,
                "email": email,
                "password": password,
                "status": "already_seeded",
            }

        patients = [
            Patient(
                doctor_id=doctor.id,
                name="Ananya Rao",
                age=58,
                gender="Female",
                contact_number="+91-90000-10001",
                blood_group="B+",
                allergies="Penicillin",
                chronic_conditions="Type 2 diabetes, hypertension",
                current_medications="Metformin 500 mg twice daily, Amlodipine 5 mg daily",
                notes="Monitor HbA1c and blood pressure at each follow-up.",
            ),
            Patient(
                doctor_id=doctor.id,
                name="Rohan Mehta",
                age=46,
                gender="Male",
                contact_number="+91-90000-10002",
                blood_group="O+",
                allergies="None recorded",
                chronic_conditions="Asthma",
                current_medications="Budesonide inhaler, Salbutamol inhaler as needed",
                notes="Exercise-induced symptoms reported during winter.",
            ),
        ]
        db.add_all(patients)
        db.flush()

        reports = [
            Report(
                patient_id=patients[0].id,
                filename="demo_ananya_diabetes_followup.txt",
                original_filename="Ananya Diabetes Follow-up.pdf",
                file_path="seeded-demo-record",
                file_size=0,
                mime_type="text/plain",
                extracted_text=(
                    "Follow-up notes: HbA1c is 7.8 percent. Blood pressure is "
                    "142/88 mmHg. Continue Metformin 500 mg twice daily and "
                    "Amlodipine 5 mg daily. Lifestyle counseling provided."
                ),
                report_type="Diabetes Follow-up",
                description="Seeded demo report",
                is_embedded=False,
            ),
            Report(
                patient_id=patients[1].id,
                filename="demo_rohan_asthma_review.txt",
                original_filename="Rohan Asthma Review.pdf",
                file_path="seeded-demo-record",
                file_size=0,
                mime_type="text/plain",
                extracted_text=(
                    "Asthma review: patient reports wheezing twice weekly. "
                    "Continue budesonide inhaler and salbutamol as needed. "
                    "Spirometry recommended if symptoms worsen."
                ),
                report_type="Asthma Review",
                description="Seeded demo report",
                is_embedded=False,
            ),
        ]
        db.add_all(reports)
        db.flush()

        session = ChatSession(
            doctor_id=doctor.id,
            patient_id=patients[0].id,
            title="Diabetes follow-up summary",
        )
        db.add(session)
        db.flush()

        db.add_all(
            [
                ChatMessage(
                    session_id=session.id,
                    role="user",
                    content="What is the latest HbA1c in the record?",
                ),
                ChatMessage(
                    session_id=session.id,
                    role="assistant",
                    content=(
                        "The latest HbA1c in the available record is 7.8 percent.\n\n"
                        "Source: Patient Medical Records"
                    ),
                    sources='["Follow-up notes: HbA1c is 7.8 percent."]',
                ),
            ]
        )

        db.commit()
        return {
            "doctor_id": doctor.id,
            "patients": len(patients),
            "reports": len(reports),
            "email": email,
            "password": password,
            "status": "seeded",
        }
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print(seed_demo_data())
    print(seed_demo_data(email=ADMIN_EMAIL, password=ADMIN_PASSWORD, name="Dr. Admin"))
