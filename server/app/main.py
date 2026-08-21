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

# ==========================================
# 商业功能：将需求表单数据导出为 Excel (带 BOM 头的 CSV)
# ==========================================
@app.get("/api/requirements/export")
def export_requirements_csv():
    import csv, io, sqlite3, os
    from fastapi.responses import StreamingResponse
    
    # 动态定位数据库绝对路径，防止终端启动位置不同导致找不到库
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "editform.db")
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM requirements")
        rows = cursor.fetchall()
    except Exception as e:
        return {"error": "无法读取数据，可能表还未创建: " + str(e)}
    finally:
        conn.close()
        
    stream = io.StringIO()
    stream.write('\ufeff') # 核心知识点：主动写入 BOM 头，Excel 打开绝对不乱码！
    writer = csv.writer(stream)
    
    if rows:
        writer.writerow(rows[0].keys()) # 写入表头 (列名)
        for row in rows:
            writer.writerow(row)        # 写入真实数据
    else:
        writer.writerow(["目前暂无客户提交需求"])
        
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=requirements_export.csv"
    return response
