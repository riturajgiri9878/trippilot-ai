from app.graph.state import TravelState
from app.models.results import StayResult


def stay_agent(state: TravelState) -> TravelState:
    request = state["request"]

    stay = StayResult(
        property_name="Mock Beach Resort",
        location=request.destination,
        price_per_night=2200,
        total_price=8800,
        currency=request.currency,
        rating=4.2,
        provider="local_mock",
        source_type="mock",
    )

    state["stays"] = [stay]

    return state