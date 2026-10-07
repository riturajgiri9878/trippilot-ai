from app.graph.state import create_initial_state
from app.graph.travel_graph import travel_graph
from app.models.trip import TripRequest

import app.graph.travel_graph as travel_graph_module


def test_travel_graph_complete_flow():
    trip = TripRequest(
        origin="Kolkata",
        destination="Goa",
        start_date="2026-12-10",
        end_date="2026-12-14",
        travelers=2,
        budget=30000,
        preferences=["Beach", "Food"],
    )

    initial_state = create_initial_state(trip)

    result = travel_graph.invoke(initial_state)

    assert len(result["flights"]) == 1
    assert len(result["stays"]) == 1
    assert len(result["activities"]) == 1

    assert result["budget"] is not None
    assert result["budget"].total_cost == 15800
    assert result["budget"].status == "WITHIN_BUDGET"

    assert len(result["itinerary"]) == 5

    assert result["warnings"] == []
    assert result["errors"] == []


def test_graph_uses_fallback_when_primary_flight_agent_fails(monkeypatch):
    def failing_primary_agent(state):
        raise RuntimeError("Simulated primary provider failure")

    monkeypatch.setattr(
        travel_graph_module,
        "flight_agent",
        failing_primary_agent,
    )

    trip = TripRequest(
        origin="Kolkata",
        destination="Goa",
        start_date="2026-12-10",
        end_date="2026-12-14",
        travelers=2,
        budget=30000,
        preferences=["Beach", "Food"],
    )

    initial_state = create_initial_state(trip)

    result = travel_graph_module.travel_graph.invoke(initial_state)

    assert len(result["flights"]) == 1

    flight = result["flights"][0]

    assert flight.provider == "local_fallback"
    assert flight.source_type == "fallback"

    assert len(result["stays"]) == 1
    assert len(result["activities"]) == 1

    assert result["budget"] is not None
    assert result["budget"].total_cost == 15800

    assert (
        "Primary flight source unavailable. Using fallback data."
        in result["warnings"]
    )

    assert len(result["errors"]) == 1
    assert result["errors"][0]["agent"] == "flight_agent"
    assert result["errors"][0]["stage"] == "primary"
    assert result["errors"][0]["error"] == "RuntimeError"


def test_graph_continues_when_primary_and_fallback_flight_agents_fail(
    monkeypatch,
):
    def failing_primary_agent(state):
        raise RuntimeError("Simulated primary provider failure")

    def failing_fallback_agent(state):
        raise RuntimeError("Simulated fallback provider failure")

    monkeypatch.setattr(
        travel_graph_module,
        "flight_agent",
        failing_primary_agent,
    )

    monkeypatch.setattr(
        travel_graph_module,
        "fallback_flight_agent",
        failing_fallback_agent,
    )

    trip = TripRequest(
        origin="Kolkata",
        destination="Goa",
        start_date="2026-12-10",
        end_date="2026-12-14",
        travelers=2,
        budget=30000,
        preferences=["Beach", "Food"],
    )

    initial_state = create_initial_state(trip)

    result = travel_graph_module.travel_graph.invoke(initial_state)

    assert result["flights"] == []

    assert len(result["stays"]) == 1
    assert len(result["activities"]) == 1

    assert result["budget"] is not None
    assert result["budget"].total_cost == 9300
    assert result["budget"].status == "WITHIN_BUDGET"

    assert len(result["itinerary"]) == 5

    assert (
        "Primary flight source unavailable. Using fallback data."
        in result["warnings"]
    )

    assert (
        "Flight information is currently unavailable."
        in result["warnings"]
    )

    assert len(result["errors"]) == 2

    assert result["errors"][0]["agent"] == "flight_agent"
    assert result["errors"][0]["stage"] == "primary"
    assert result["errors"][0]["error"] == "RuntimeError"

    assert result["errors"][1]["agent"] == "flight_agent"
    assert result["errors"][1]["stage"] == "fallback"
    assert result["errors"][1]["error"] == "RuntimeError"