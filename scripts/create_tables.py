from app.database.base import Base
from app.database.database import engine
from app.database.models import TripRecord


def create_tables() -> None:
    Base.metadata.create_all(
        bind=engine
    )

    print("Database tables created successfully.")


if __name__ == "__main__":
    create_tables()