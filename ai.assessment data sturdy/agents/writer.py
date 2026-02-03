# agents/writer.py

import requests

MCP_BASE_URL = "http://127.0.0.1:8000/tool"


def writer_agent(competitors, impact_radar, sources):
    """
    Report Writer Agent:
    Produces final structured market report
    """

    payload = {
        "competitors": competitors,
        "impact_radar": impact_radar,
        "sources": sources
    }

    response = requests.post(
        f"{MCP_BASE_URL}/generate_market_report",
        json={"data": payload}
    )

    return response.json()
