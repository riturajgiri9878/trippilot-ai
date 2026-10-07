from app.graph.state import TravelState
from app.tools.stay_tool import search_stays


def stay_agent(state: TravelState) -> TravelState:
    request = state["request"]

    state["stays"] = search_stays(request)

    return state