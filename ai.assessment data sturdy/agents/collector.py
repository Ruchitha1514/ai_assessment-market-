# agents/collector.py

import requests

MCP_BASE_URL = "http://127.0.0.1:8000/tool"


def collector_agent(industry: str, start_date: str, end_date: str):
    """
    Collector Agent:
    Finds relevant news, regulatory updates, and signals
    """

    query = f"{industry} regulatory updates between {start_date} and {end_date}"

    response = requests.post(
        f"{MCP_BASE_URL}/search_web",
        json={"query": query}
    )

    results = response.json()
    return results
