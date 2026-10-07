from app.graph.state import TravelState, create_initial_state
from app.graph.travel_graph import travel_graph
from app.models.trip import TripRequest


def plan_trip(request: TripRequest) -> TravelState:
    initial_state = create_initial_state(request)

    result = travel_graph.invoke(initial_state)

    return result