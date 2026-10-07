from app.graph.state import TravelState
from app.models.results import ActivityResult


def activity_agent(state: TravelState) -> TravelState:
    request = state["request"]

    activity = ActivityResult(
        name="Beach Sightseeing",
        category="Sightseeing",
        location=request.destination,
        estimated_cost=500,
        estimated_duration_hours=2,
        provider="local_mock",
        source_type="mock",
    )

    state["activities"] = [activity]

    return state