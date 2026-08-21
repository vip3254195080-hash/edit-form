from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from app.database import get_db, init_db

app = FastAPI(title="EditForm API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

class RequirementCreate(BaseModel):
    client_name: str
    contact_info: str
    video_type: str
    duration: Optional[str] = "未填写"
    budget: Optional[str] = "面议"
    material_url: Optional[str] = ""
    reference_url: Optional[str] = ""
    notes: Optional[str] = ""

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "EditForm Backend", "code": 200}

@app.post("/api/requirements")
def create_requirement(req: RequirementCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO requirements (client_name, contact_info, video_type, duration, budget, material_url, reference_url, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (req.client_name, req.contact_info, req.video_type, req.duration, req.budget, req.material_url, req.reference_url, req.notes))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"code": 200, "message": "提交成功", "data": {"id": new_id}}

@app.get("/api/requirements")
def list_requirements():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM requirements ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return {"code": 200, "data": [dict(row) for row in rows]}
