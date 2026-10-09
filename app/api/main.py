from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app.config import settings
from app.database.base import Base
from app.database.database import SessionLocal, engine
from app.database.models import TripRecord
from app.database.trip_repository import get_trip, list_trips
from app.models.trip import TripRequest
from app.services.trip_planner import plan_trip_and_save


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description=(
        "TripPilot AI - Multi-Agent Travel Planner API"
    ),
    lifespan=lifespan,
)


def serialize_trip(
    trip: TripRecord,
) -> dict[str, Any]:
    return {
        "id": trip.id,
        "origin": trip.origin,
        "destination": trip.destination,
        "start_date": trip.start_date.isoformat(),
        "end_date": trip.end_date.isoformat(),
        "travelers": trip.travelers,
        "budget": trip.budget,
        "currency": trip.currency,
        "preferences": trip.preferences,
        "status": trip.status,
        "plan_data": trip.plan_data,
        "created_at": (
            trip.created_at.isoformat()
            if trip.created_at
            else None
        ),
    }


@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "message": "TripPilot AI API is running.",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/ready")
def readiness():
    database = SessionLocal()

    try:
        database.execute(
            text("SELECT 1")
        )

        return {
            "status": "ready",
            "database": "connected",
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database is not ready.",
        )

    finally:
        database.close()


@app.post("/api/v1/trips/plan")
def create_trip_plan(
    request: TripRequest,
):
    try:
        trip_id, plan = plan_trip_and_save(
            request
        )

        saved_trip = get_trip(
            trip_id
        )

        if saved_trip is None:
            raise HTTPException(
                status_code=500,
                detail="Trip was planned but could not be loaded.",
            )

        return {
            "trip_id": trip_id,
            "status": saved_trip.status,
            "plan": plan,
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to create trip plan.",
        )


@app.get("/api/v1/trips")
def get_all_trips():
    trips = list_trips()

    return {
        "count": len(trips),
        "trips": [
            serialize_trip(trip)
            for trip in trips
        ],
    }


@app.get("/api/v1/trips/{trip_id}")
def get_trip_by_id(
    trip_id: int,
):
    trip = get_trip(
        trip_id
    )

    if trip is None:
        raise HTTPException(
            status_code=404,
            detail="Trip not found.",
        )

    return serialize_trip(
        trip
    )