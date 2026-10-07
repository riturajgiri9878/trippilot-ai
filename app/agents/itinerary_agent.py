from datetime import timedelta

from app.graph.state import TravelState


def itinerary_agent(state: TravelState) -> TravelState:
    request = state["request"]

    trip_days = (request.end_date - request.start_date).days + 1

    itinerary = []

    for day_index in range(trip_days):
        current_date = request.start_date + timedelta(days=day_index)

        if day_index == 0:
            activities = [
                "Travel to destination",
                "Hotel check-in",
                "Relax and explore nearby area",
            ]

        elif day_index == trip_days - 1:
            activities = [
                "Check out from hotel",
                "Final local visit",
                "Return journey",
            ]

        else:
            activities = [
                "Morning sightseeing",
                "Lunch / local food",
                "Evening activity",
            ]

        itinerary.append(
            {
                "day": day_index + 1,
                "date": current_date.isoformat(),
                "activities": activities,
            }
        )

    state["itinerary"] = itinerary

    return state