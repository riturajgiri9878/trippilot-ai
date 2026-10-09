from datetime import date, datetime, timezone

from fastapi.testclient import TestClient

import app.api.main as api_main


client = TestClient(api_main.app)


class FakeTrip:
    def __init__(
        self,
        trip_id: int = 1,
        origin: str = "Kolkata",
        destination: str = "Goa",
        status: str = "PLANNED",
    ):
        self.id = trip_id
        self.origin = origin
        self.destination = destination
        self.start_date = date(2026, 12, 10)
        self.end_date = date(2026, 12, 14)
        self.travelers = 2
        self.budget = 30000.0
        self.currency = "INR"
        self.preferences = ["Beach", "Food"]
        self.status = status
        self.plan_data = {
            "warnings": [],
            "errors": [],
        }
        self.created_at = datetime(
            2026,
            10,
            9,
            tzinfo=timezone.utc,
        )


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["app"] == "TripPilot AI"
    assert data["message"] == (
        "TripPilot AI API is running."
    )


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }


def test_ready(
    monkeypatch,
):
    class FakeDatabase:
        def execute(
            self,
            query,
        ):
            return True

        def close(
            self,
        ):
            pass

    monkeypatch.setattr(
        api_main,
        "SessionLocal",
        lambda: FakeDatabase(),
    )

    response = client.get("/ready")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ready",
        "database": "connected",
    }


def test_create_trip_plan(
    monkeypatch,
):
    fake_trip = FakeTrip(
        trip_id=99,
    )

    fake_plan = {
        "flights": [
            {
                "airline": "Mock Airways",
                "price": 6500,
            }
        ],
        "stays": [],
        "activities": [],
        "weather": {},
        "currency_conversion": {},
        "budget": {
            "total_cost": 15800,
        },
        "itinerary": [],
        "warnings": [],
        "errors": [],
    }

    def fake_plan_trip_and_save(
        request,
    ):
        return 99, fake_plan

    monkeypatch.setattr(
        api_main,
        "plan_trip_and_save",
        fake_plan_trip_and_save,
    )

    monkeypatch.setattr(
        api_main,
        "get_trip",
        lambda trip_id: fake_trip,
    )

    response = client.post(
        "/api/v1/trips/plan",
        json={
            "origin": "Kolkata",
            "destination": "Goa",
            "start_date": "2026-12-10",
            "end_date": "2026-12-14",
            "travelers": 2,
            "budget": 30000,
            "currency": "INR",
            "preferences": [
                "Beach",
                "Food",
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["trip_id"] == 99
    assert data["status"] == "PLANNED"
    assert (
        data["plan"]["budget"]["total_cost"]
        == 15800
    )


def test_list_trips(
    monkeypatch,
):
    trips = [
        FakeTrip(
            trip_id=2,
            origin="Delhi",
            destination="Mumbai",
        ),
        FakeTrip(
            trip_id=1,
            origin="Kolkata",
            destination="Goa",
        ),
    ]

    monkeypatch.setattr(
        api_main,
        "list_trips",
        lambda: trips,
    )

    response = client.get(
        "/api/v1/trips"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 2
    assert data["trips"][0]["id"] == 2
    assert data["trips"][1]["id"] == 1


def test_get_trip_by_id(
    monkeypatch,
):
    fake_trip = FakeTrip(
        trip_id=7,
    )

    monkeypatch.setattr(
        api_main,
        "get_trip",
        lambda trip_id: fake_trip,
    )

    response = client.get(
        "/api/v1/trips/7"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 7
    assert data["origin"] == "Kolkata"
    assert data["destination"] == "Goa"


def test_get_trip_not_found(
    monkeypatch,
):
    monkeypatch.setattr(
        api_main,
        "get_trip",
        lambda trip_id: None,
    )

    response = client.get(
        "/api/v1/trips/999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Trip not found.",
    }


def test_invalid_trip_request():
    response = client.post(
        "/api/v1/trips/plan",
        json={
            "origin": "Kolkata",
            "destination": "Goa",
            "start_date": "2026-12-14",
            "end_date": "2026-12-10",
            "travelers": 0,
            "budget": -100,
            "currency": "INR",
            "preferences": [],
        },
    )

    assert response.status_code == 422