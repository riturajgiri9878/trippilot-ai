from datetime import date, datetime
from typing import Any

from app.database.database import SessionLocal
from app.database.models import TripRecord
from app.models.trip import TripRequest


def _make_json_safe(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")

    if isinstance(value, dict):
        return {
            key: _make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _make_json_safe(item)
            for item in value
        ]

    if isinstance(value, (date, datetime)):
        return value.isoformat()

    return value


def save_trip(
    request: TripRequest,
    plan_data: dict[str, Any] | None = None,
    status: str = "PLANNED",
) -> TripRecord:
    database = SessionLocal()

    try:
        trip = TripRecord(
            origin=request.origin,
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            travelers=request.travelers,
            budget=request.budget,
            currency=request.currency,
            preferences=request.preferences,
            plan_data=(
                _make_json_safe(plan_data)
                if plan_data
                else None
            ),
            status=status,
        )

        database.add(trip)
        database.commit()
        database.refresh(trip)

        return trip

    except Exception:
        database.rollback()
        raise

    finally:
        database.close()


def get_trip(
    trip_id: int,
) -> TripRecord | None:
    database = SessionLocal()

    try:
        return database.get(
            TripRecord,
            trip_id,
        )

    finally:
        database.close()


def list_trips() -> list[TripRecord]:
    database = SessionLocal()

    try:
        return (
            database.query(TripRecord)
            .order_by(TripRecord.id.desc())
            .all()
        )

    finally:
        database.close()