Agentic Market Intelligence System

An agent-based backend system that generates structured market intelligence reports using a multi-agent architecture with strict separation between reasoning and execution.

Overview
>Multi-agent design (Collector, Extractor, Impact, Writer)
>MCP-based tool execution
>LangGraph orchestration
>FastAPI REST APIs
>SQLite storage
>Open-source only

Project Structure
agents/        - AI agents
mcp_server/    - MCP tools & server
orchestration/ - LangGraph workflow
api/           - REST API layer
sample_output/ - report.json
logs/          - execution logs

APIs

POST /analyze – Generate market report

POST /chat – Query generated report

GET /health – Health check

How to Run
1. Install dependencies
python -m pip install -r requirements.txt

2. Start MCP Server
python -m uvicorn mcp_server.server:app --reload

3. Start API Server (new terminal)
python -m uvicorn api.main:app --reload --port 9000

Sample Output

Generated report:

sample_output/report.json

Logs
logs/execution.log
