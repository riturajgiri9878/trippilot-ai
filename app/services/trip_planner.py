from app.database.trip_repository import save_trip
from app.graph.state import TravelState, create_initial_state
from app.graph.travel_graph import travel_graph
from app.models.trip import TripRequest


def plan_trip(
    request: TripRequest,
) -> TravelState:
    initial_state = create_initial_state(
        request
    )

    result = travel_graph.invoke(
        initial_state
    )

    return result


def plan_trip_and_save(
    request: TripRequest,
) -> tuple[int, TravelState]:
    result = plan_trip(
        request
    )

    if result["warnings"]:
        status = "PLANNED_WITH_WARNINGS"
    else:
        status = "PLANNED"

    saved_trip = save_trip(
        request=request,
        plan_data=result,
        status=status,
    )

    return saved_trip.id, result