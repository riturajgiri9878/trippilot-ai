from app.graph.state import TravelState
from app.tools.activity_tool import search_activities


def activity_agent(state: TravelState) -> TravelState:
    request = state["request"]

    state["activities"] = search_activities(request)

    return state