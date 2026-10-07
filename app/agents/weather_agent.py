from app.graph.state import TravelState
from app.tools.weather_tool import get_weather


def weather_agent(state: TravelState) -> TravelState:
    request = state["request"]

    state["weather"] = get_weather(
        request.destination,
        "IN",
    )

    return state