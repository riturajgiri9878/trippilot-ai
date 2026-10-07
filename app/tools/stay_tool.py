from app.models.results import StayResult
from app.models.trip import TripRequest


def search_stays(request: TripRequest) -> list[StayResult]:
    return [
        StayResult(
            property_name="Mock Beach Resort",
            location=request.destination,
            price_per_night=2200,
            total_price=8800,
            currency=request.currency,
            rating=4.2,
            provider="local_mock",
            source_type="mock",
        )
    ]