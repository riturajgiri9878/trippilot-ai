from app.graph.state import TravelState
from app.tools.flight_tool import (
    search_fallback_flights,
    search_primary_flights,
)


def flight_agent(state: TravelState) -> TravelState:
    request = state["request"]

    state["flights"] = search_primary_flights(request)

    return state


def fallback_flight_agent(state: TravelState) -> TravelState:
    request = state["request"]

    state["flights"] = search_fallback_flights(request)

    return state