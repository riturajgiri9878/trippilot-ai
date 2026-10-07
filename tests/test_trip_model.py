import pytest
from pydantic import ValidationError

from app.models.trip import TripRequest


def test_valid_trip_request():
    trip = TripRequest(
        origin="Kolkata",
        destination="Goa",
        start_date="2026-12-10",
        end_date="2026-12-14",
        travelers=2,
        budget=30000,
        currency="inr",
        preferences=["Beach", "Food"],
    )

    assert trip.origin == "Kolkata"
    assert trip.destination == "Goa"
    assert trip.travelers == 2
    assert trip.budget == 30000
    assert trip.currency == "INR"


def test_invalid_traveler_count():
    with pytest.raises(ValidationError):
        TripRequest(
            origin="Kolkata",
            destination="Goa",
            start_date="2026-12-10",
            end_date="2026-12-14",
            travelers=0,
            budget=30000,
        )


def test_invalid_budget():
    with pytest.raises(ValidationError):
        TripRequest(
            origin="Kolkata",
            destination="Goa",
            start_date="2026-12-10",
            end_date="2026-12-14",
            travelers=2,
            budget=0,
        )


def test_invalid_date_order():
    with pytest.raises(ValidationError):
        TripRequest(
            origin="Kolkata",
            destination="Goa",
            start_date="2026-12-20",
            end_date="2026-12-10",
            travelers=2,
            budget=30000,
        )


def test_currency_is_uppercase():
    trip = TripRequest(
        origin="Kolkata",
        destination="Goa",
        start_date="2026-12-10",
        end_date="2026-12-14",
        travelers=2,
        budget=30000,
        currency="usd",
    )

    assert trip.currency == "USD"