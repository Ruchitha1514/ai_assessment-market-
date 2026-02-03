# api/main.py
# Market Intelligence API - Final Correct Version

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import json
import uuid

from orchestration.graph import build_graph


# --------------------------------------------------
# FastAPI App
# --------------------------------------------------
app = FastAPI(title="Market Intelligence API")


# --------------------------------------------------
# Database Configuration
# --------------------------------------------------
DB_PATH = "storage/reports.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            report_id TEXT PRIMARY KEY,
            report_json TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


# --------------------------------------------------
# Request Models
# --------------------------------------------------
class AnalyzeRequest(BaseModel):
    industry: str
    from_date: str
    to_date: str
    focus: str | None = None


class ChatRequest(BaseModel):
    report_id: str
    question: str


# --------------------------------------------------
# /analyze Endpoint
# --------------------------------------------------
@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    graph = build_graph()

    # Initial state for LangGraph
    initial_state = {
        "industry": req.industry,
        "from_date": req.from_date,
        "to_date": req.to_date
    }

    # Run agentic pipeline
    result = graph.invoke(initial_state)

    report = result["final_report"]

    # Generate unique report ID
    report_id = str(uuid.uuid4())

    # Store report in SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO reports (report_id, report_json) VALUES (?, ?)",
        (report_id, json.dumps(report))
    )
    conn.commit()
    conn.close()

    # RETURN BOTH report_id AND report (IMPORTANT)
    return {
        "report_id": report_id,
        "report": report
    }


# --------------------------------------------------
# /chat Endpoint
# --------------------------------------------------
@app.post("/chat")
def chat(req: ChatRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT report_json FROM reports WHERE report_id = ?",
        (req.report_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {"error": "Report not found"}

    report = json.loads(row[0])

    # Answer strictly from report context
    answer = f"""
Summary:
{report.get("summary")}

Key Risks:
{", ".join(report.get("risks", []))}

Key Opportunities:
{", ".join(report.get("opportunities", []))}
""".strip()

    return {
        "answer": answer,
        "citations": report.get("sources", [])
    }


# --------------------------------------------------
# Health Check
# --------------------------------------------------
@app.get("/health")
def health():
    return {"status": "API Server is running"}
