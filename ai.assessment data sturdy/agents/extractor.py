# agents/extractor.py

import requests

MCP_BASE_URL = "http://127.0.0.1:8000/tool"


def extractor_agent(items):
    """
    Extractor Agent:
    Fetches content and extracts entities
    """

    all_competitors = set()
    sources = []

    for item in items:
        url = item.get("url")
        if not url:
            continue

        # Fetch raw content
        raw = requests.post(
            f"{MCP_BASE_URL}/fetch_url",
            json={"url": url}
        ).json()

        # Clean content
        cleaned = requests.post(
            f"{MCP_BASE_URL}/clean_extract",
            json={"raw_text": raw}
        ).json()

        # Extract entities
        entities = requests.post(
            f"{MCP_BASE_URL}/extract_entities",
            json={"text": cleaned}
        ).json()

        for comp in entities.get("competitors", []):
            all_competitors.add(comp)

        sources.append(url)

    return {
        "competitors": list(all_competitors),
        "sources": sources
    }
