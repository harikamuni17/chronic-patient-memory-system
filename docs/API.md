# Chronic Patient Memory System — API Reference

Base URL (local): `http://localhost:8000/api/v1`  
Base URL (production): `https://your-app.onrender.com/api/v1`

Interactive docs: `GET /docs` (Swagger UI) | `GET /redoc`

---

## Authentication

All protected endpoints require the header:
```
Authorization: Bearer <access_token>
```

### POST `/auth/login`
Login with email + password (OAuth2 form).

**Request** (`application/x-www-form-urlencoded`)
| Field | Type | Notes |
|---|---|---|
| `username` | string | Doctor's email |
| `password` | string | Plain text password |

**Response 200**
```json
{ "access_token": "eyJ...", "token_type": "bearer" }
```

---

### POST `/auth/register`
Register a new doctor account.

**Request** (`application/json`)
```json
{ "name": "Dr. Jane Smith", "email": "jane@hospital.com", "password": "Str0ng#Pass" }
```

**Response 201**
```json
{ "id": 1, "name": "Dr. Jane Smith", "email": "jane@hospital.com", "is_active": true, ... }
```

---

### GET `/auth/me`
Get the current authenticated doctor's profile.

**Response 200** — `UserResponse` object

---

## Patients

### GET `/patients/`
List all patients for the authenticated doctor.

**Query params**: `skip`, `limit`, `search` (name filter)

**Response 200**
```json
{ "total": 42, "patients": [ { "id": 1, "name": "John Doe", ... } ] }
```

---

### POST `/patients/`
Create a new patient.

**Request**
```json
{
  "name": "John Doe", "age": 45, "gender": "Male",
  "blood_group": "O+", "chronic_conditions": "Type 2 Diabetes, Hypertension",
  "current_medications": "Metformin 500mg, Lisinopril 10mg"
}
```

**Response 201** — full `PatientResponse`

---

### GET `/patients/stats`
Returns dashboard statistics for the current doctor.

**Response 200**
```json
{ "total_patients": 10, "total_reports": 35, "total_chat_sessions": 18 }
```

---

### GET `/patients/{patient_id}`
Get a single patient by ID.

---

### PATCH `/patients/{patient_id}`
Partially update a patient (all fields optional).

---

### DELETE `/patients/{patient_id}`
Delete patient + all reports + ChromaDB embeddings. Returns `204 No Content`.

---

## Reports (PDF Upload)

### POST `/patients/{patient_id}/reports/`
Upload a PDF medical report.

**Request** (`multipart/form-data`)
| Field | Type | Notes |
|---|---|---|
| `file` | file | PDF only, max 20 MB |
| `report_type` | string (optional) | e.g. "Blood Test", "MRI" |
| `description` | string (optional) | Free text note |

**Response 201**
```json
{
  "id": 1, "patient_id": 5,
  "original_filename": "bloodtest_jan.pdf",
  "is_embedded": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

`is_embedded: true` means the PDF has been indexed in ChromaDB and is available for AI queries.

---

### GET `/patients/{patient_id}/reports/`
List all reports for a patient (newest first).

---

### DELETE `/reports/{report_id}`
Delete a report, its physical file, and its ChromaDB embeddings.

---

## Chat (AI / RAG)

### POST `/patients/{patient_id}/sessions/`
Create a new chat session.

**Request**
```json
{ "title": "Follow-up consultation" }
```

---

### GET `/patients/{patient_id}/sessions/`
List all sessions for a patient (newest first).

---

### GET `/sessions/{session_id}/messages/`
Retrieve the full conversation history of a session.

---

### POST `/sessions/{session_id}/ask`
**Ask the AI a question about the patient's medical records.**

**Request**
```json
{ "question": "What medications is this patient currently taking?" }
```

**Response 200**
```json
{
  "session_id": 3,
  "question_message": { "id": 7, "role": "user", "content": "What medications..." },
  "answer_message": {
    "id": 8,
    "role": "assistant",
    "content": "Based on the patient's records:\n• Metformin 500mg...\n\nSource: Patient Medical Records",
    "sources": "[\"...chunk 1...\", \"...chunk 2...\"]"
  }
}
```

---

## Error Responses

| Code | Meaning |
|---|---|
| 400 | Bad request (validation error, file too large, wrong type) |
| 401 | Unauthenticated — missing or invalid JWT |
| 403 | Forbidden |
| 404 | Resource not found |
| 409 | Conflict (e.g. duplicate email) |
| 503 | AI service temporarily unavailable |

---

## Health Check

### GET `/health`
Returns `{ "status": "ok" }` — used by Render.com for deployment health checks.
