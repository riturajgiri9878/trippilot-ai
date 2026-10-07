from langgraph.graph import END, START, StateGraph

from app.agents.activity_agent import activity_agent
from app.agents.budget_agent import budget_agent
from app.agents.flight_agent import (
    fallback_flight_agent,
    flight_agent,
)
from app.agents.itinerary_agent import itinerary_agent
from app.agents.stay_agent import stay_agent
from app.agents.weather_agent import weather_agent
from app.graph.state import TravelState


def safe_flight_agent(
    state: TravelState,
) -> TravelState:
    try:
        return flight_agent(state)

    except Exception as primary_error:
        state["errors"].append(
            {
                "agent": "flight_agent",
                "stage": "primary",
                "error": type(primary_error).__name__,
            }
        )

        state["warnings"].append(
            "Primary flight source unavailable. "
            "Using fallback data."
        )

        try:
            return fallback_flight_agent(state)

        except Exception as fallback_error:
            state["errors"].append(
                {
                    "agent": "flight_agent",
                    "stage": "fallback",
                    "error": type(
                        fallback_error
                    ).__name__,
                }
            )

            state["warnings"].append(
                "Flight information is currently "
                "unavailable."
            )

            state["flights"] = []

            return state


def safe_weather_agent(
    state: TravelState,
) -> TravelState:
    try:
        return weather_agent(state)

    except Exception as error:
        state["errors"].append(
            {
                "agent": "weather_agent",
                "stage": "live_provider",
                "error": type(error).__name__,
            }
        )

        state["warnings"].append(
            "Live weather information is currently "
            "unavailable."
        )

        state["weather"] = {}

        return state


def build_travel_graph():
    graph = StateGraph(TravelState)

    graph.add_node(
        "flight_agent",
        safe_flight_agent,
    )

    graph.add_node(
        "stay_agent",
        stay_agent,
    )

    graph.add_node(
        "activity_agent",
        activity_agent,
    )

    graph.add_node(
        "weather_agent",
        safe_weather_agent,
    )

    graph.add_node(
        "budget_agent",
        budget_agent,
    )

    graph.add_node(
        "itinerary_agent",
        itinerary_agent,
    )

    graph.add_edge(
        START,
        "flight_agent",
    )

    graph.add_edge(
        "flight_agent",
        "stay_agent",
    )

    graph.add_edge(
        "stay_agent",
        "activity_agent",
    )

    graph.add_edge(
        "activity_agent",
        "weather_agent",
    )

    graph.add_edge(
        "weather_agent",
        "budget_agent",
    )

    graph.add_edge(
        "budget_agent",
        "itinerary_agent",
    )

    graph.add_edge(
        "itinerary_agent",
        END,
    )

    return graph.compile()


travel_graph = build_travel_graph()