# agents/impact.py

import requests

MCP_BASE_URL = "http://127.0.0.1:8000/tool"


def impact_agent(items, context: str):
    """
    Impact Agent:
    Assigns impact score and actions
    """

    impact_results = []

    for item in items:
        response = requests.post(
            f"{MCP_BASE_URL}/impact_score",
            json={
                "item": item,
                "context": context
            }
        )

        impact_results.append(response.json())

    return impact_results
