from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.database.trip_repository as trip_repository_module

from app.database.base import Base
from app.models.trip import TripRequest


def create_test_database(
    tmp_path,
    monkeypatch,
):
    database_path = tmp_path / "test_trippilot.db"

    engine = create_engine(
        f"sqlite:///{database_path}",
        connect_args={
            "check_same_thread": False,
        },
    )

    TestSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(
        bind=engine,
    )

    monkeypatch.setattr(
        trip_repository_module,
        "SessionLocal",
        TestSessionLocal,
    )

    return engine


def create_test_trip() -> TripRequest:
    return TripRequest(
        origin="Kolkata",
        destination="Goa",
        start_date="2026-12-10",
        end_date="2026-12-14",
        travelers=2,
        budget=30000,
        currency="INR",
        preferences=["Beach", "Food"],
    )


def test_save_and_get_trip(
    tmp_path,
    monkeypatch,
):
    engine = create_test_database(
        tmp_path,
        monkeypatch,
    )

    trip_request = create_test_trip()

    saved_trip = trip_repository_module.save_trip(
        trip_request,
    )

    assert saved_trip.id == 1

    loaded_trip = trip_repository_module.get_trip(
        saved_trip.id,
    )

    assert loaded_trip is not None
    assert loaded_trip.origin == "Kolkata"
    assert loaded_trip.destination == "Goa"
    assert loaded_trip.travelers == 2
    assert loaded_trip.budget == 30000
    assert loaded_trip.currency == "INR"
    assert loaded_trip.status == "PLANNED"

    engine.dispose()


def test_list_trips(
    tmp_path,
    monkeypatch,
):
    engine = create_test_database(
        tmp_path,
        monkeypatch,
    )

    first_trip = create_test_trip()

    second_trip = TripRequest(
        origin="Delhi",
        destination="Mumbai",
        start_date="2026-11-01",
        end_date="2026-11-04",
        travelers=1,
        budget=20000,
        currency="INR",
        preferences=["Food"],
    )

    trip_repository_module.save_trip(
        first_trip,
    )

    trip_repository_module.save_trip(
        second_trip,
    )

    trips = trip_repository_module.list_trips()

    assert len(trips) == 2

    assert trips[0].origin == "Delhi"
    assert trips[0].destination == "Mumbai"

    assert trips[1].origin == "Kolkata"
    assert trips[1].destination == "Goa"

    engine.dispose()


def test_plan_data_is_saved_as_json(
    tmp_path,
    monkeypatch,
):
    engine = create_test_database(
        tmp_path,
        monkeypatch,
    )

    trip_request = create_test_trip()

    plan_data = {
        "weather": {
            "provider": "open_meteo",
            "temperature_c": 30.0,
        },
        "currency_conversion": {
            "provider": "frankfurter",
            "converted_currency": "USD",
        },
        "warnings": [],
        "errors": [],
    }

    saved_trip = trip_repository_module.save_trip(
        trip_request,
        plan_data=plan_data,
    )

    loaded_trip = trip_repository_module.get_trip(
        saved_trip.id,
    )

    assert loaded_trip is not None
    assert loaded_trip.plan_data is not None

    assert (
        loaded_trip.plan_data["weather"]["provider"]
        == "open_meteo"
    )

    assert (
        loaded_trip.plan_data[
            "currency_conversion"
        ]["provider"]
        == "frankfurter"
    )

    engine.dispose()