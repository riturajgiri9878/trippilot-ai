from datetime import timedelta

from app.graph.state import TravelState


def itinerary_agent(
    state: TravelState,
) -> TravelState:
    request = state["request"]

    stays = state.get(
        "stays",
        [],
    )

    activities = state.get(
        "activities",
        [],
    )

    hotel_name = (
        stays[0].property_name
        if stays
        else "selected hotel"
    )

    hotel_location = (
        stays[0].location
        if stays
        else request.destination
    )

    activity_names = [
        activity.name
        for activity in activities
    ]

    total_days = (
        request.end_date
        - request.start_date
    ).days + 1

    itinerary = []

    for index in range(
        total_days
    ):
        day_number = index + 1

        current_date = (
            request.start_date
            + timedelta(days=index)
        )

        if day_number == 1:
            day_activities = [
                (
                    f"Travel from "
                    f"{request.origin} "
                    f"to {request.destination}"
                ),
                (
                    f"Check-in at "
                    f"{hotel_name}"
                ),
                (
                    f"Relax and explore "
                    f"near {hotel_location}"
                ),
            ]

        elif day_number == total_days:
            day_activities = [
                (
                    f"Breakfast at or near "
                    f"{hotel_name}"
                ),
                (
                    f"Check-out from "
                    f"{hotel_name}"
                ),
                (
                    f"Return journey to "
                    f"{request.origin}"
                ),
            ]

        else:
            if activity_names:
                activity = activity_names[
                    (day_number - 2)
                    % len(activity_names)
                ]

                day_activities = [
                    (
                        f"Breakfast at "
                        f"{hotel_name}"
                    ),
                    activity,
                    (
                        f"Return to "
                        f"{hotel_name}"
                    ),
                ]

            else:
                day_activities = [
                    (
                        f"Breakfast at "
                        f"{hotel_name}"
                    ),
                    (
                        f"Explore "
                        f"{request.destination}"
                    ),
                    (
                        f"Return to "
                        f"{hotel_name}"
                    ),
                ]

        itinerary.append(
            {
                "day": day_number,
                "date": (
                    current_date.isoformat()
                ),
                "hotel": hotel_name,
                "activities": day_activities,
            }
        )

    state["itinerary"] = itinerary

    return state