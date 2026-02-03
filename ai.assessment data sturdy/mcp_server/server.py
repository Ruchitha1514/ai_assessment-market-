# mcp_server/server.py
# MCP Server - exposes tools to agents

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import logging

from mcp_server import tools


# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------
logging.basicConfig(
    filename="logs/execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


# --------------------------------------------------
# FastAPI App
# --------------------------------------------------
app = FastAPI(title="MCP Tool Server")


# --------------------------------------------------
# Request Models
# --------------------------------------------------
class SearchRequest(BaseModel):
    query: str


class FetchRequest(BaseModel):
    url: str


class CleanRequest(BaseModel):
    raw_text: str


class EntityRequest(BaseModel):
    text: str


class DedupeRequest(BaseModel):
    items: List[Dict]


class ImpactRequest(BaseModel):
    item: Dict
    context: str


class ReportRequest(BaseModel):
    data: Dict


# --------------------------------------------------
# MCP Tool Endpoints
# --------------------------------------------------
@app.post("/tool/search_web")
def search_web(req: SearchRequest):
    logging.info("[MCP] search_web called")
    return tools.search_web(req.query)


@app.post("/tool/fetch_url")
def fetch_url(req: FetchRequest):
    logging.info("[MCP] fetch_url called")
    return tools.fetch_url(req.url)


@app.post("/tool/clean_extract")
def clean_extract(req: CleanRequest):
    logging.info("[MCP] clean_extract called")
    return tools.clean_extract(req.raw_text)


@app.post("/tool/extract_entities")
def extract_entities(req: EntityRequest):
    logging.info("[MCP] extract_entities called")
    return tools.extract_entities(req.text)


@app.post("/tool/dedupe_items")
def dedupe_items(req: DedupeRequest):
    logging.info("[MCP] dedupe_items called")
    return tools.dedupe_items(req.items)


@app.post("/tool/impact_score")
def impact_score(req: ImpactRequest):
    logging.info("[MCP] impact_score called")
    return tools.impact_score(req.item, req.context)


@app.post("/tool/generate_market_report")
def generate_market_report(req: ReportRequest):
    logging.info("[MCP] generate_market_report called")
    return tools.generate_market_report(req.data)


# --------------------------------------------------
# Health Check
# --------------------------------------------------
@app.get("/health")
def health():
    return {"status": "MCP Server is running"}
