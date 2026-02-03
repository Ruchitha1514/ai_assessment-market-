# orchestration/graph.py
# LangGraph orchestration for Agentic Pipeline

from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END

from agents.collector import collector_agent
from agents.extractor import extractor_agent
from agents.impact import impact_agent
from agents.writer import writer_agent


# --------------------------------------------------
# Define Shared State
# --------------------------------------------------
class MarketState(TypedDict):
    industry: str
    from_date: str
    to_date: str

    collected_items: List[Dict]
    competitors: List[str]
    sources: List[str]

    impact_radar: List[Dict]
    final_report: Dict


# --------------------------------------------------
# Node 1: Collector
# --------------------------------------------------
def collector_node(state: MarketState):
    items = collector_agent(
        industry=state["industry"],
        start_date=state["from_date"],
        end_date=state["to_date"]
    )

    return {
        "collected_items": items
    }


# --------------------------------------------------
# Node 2: Extractor
# --------------------------------------------------
def extractor_node(state: MarketState):
    extracted = extractor_agent(state["collected_items"])

    return {
        "competitors": extracted["competitors"],
        "sources": extracted["sources"]
    }


# --------------------------------------------------
# Node 3: Impact Analyzer
# --------------------------------------------------
def impact_node(state: MarketState):
    impact = impact_agent(
        items=state["collected_items"],
        context=state["industry"]
    )

    return {
        "impact_radar": impact
    }


# --------------------------------------------------
# Node 4: Report Writer
# --------------------------------------------------
def writer_node(state: MarketState):
    report = writer_agent(
        competitors=state["competitors"],
        impact_radar=state["impact_radar"],
        sources=state["sources"]
    )

    return {
        "final_report": report
    }


# --------------------------------------------------
# Build LangGraph
# --------------------------------------------------
def build_graph():
    graph = StateGraph(MarketState)

    graph.add_node("collector", collector_node)
    graph.add_node("extractor", extractor_node)
    graph.add_node("impact", impact_node)
    graph.add_node("writer", writer_node)

    graph.set_entry_point("collector")

    graph.add_edge("collector", "extractor")
    graph.add_edge("extractor", "impact")
    graph.add_edge("impact", "writer")
    graph.add_edge("writer", END)

    return graph.compile()
