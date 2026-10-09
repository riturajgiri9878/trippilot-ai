import os
from datetime import date, datetime, timedelta
from typing import Any

import httpx
import streamlit as st

from app.models.trip import TripRequest
from app.services.trip_planner import plan_trip


API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "",
).strip()


st.set_page_config(
    page_title="TripPilot AI",
    page_icon="✈️",
    layout="wide",
)


def make_json_safe(
    value: Any,
) -> Any:
    """
    Convert Pydantic models and Python objects
    into normal JSON-friendly dictionaries/lists.

    This keeps the output format the same in:
    1. FastAPI mode
    2. Direct Streamlit Cloud mode
    """

    if hasattr(value, "model_dump"):
        return value.model_dump(
            mode="json"
        )

    if isinstance(value, dict):
        return {
            key: make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    if isinstance(
        value,
        (date, datetime),
    ):
        return value.isoformat()

    return value


def call_trip_planner(
    payload: dict,
) -> dict:
    """
    Two execution modes:

    API mode:
        Streamlit -> FastAPI -> LangGraph

    Direct mode:
        Streamlit -> LangGraph

    Direct mode is useful for Streamlit Community Cloud,
    where a separate FastAPI deployment is optional.
    """

    if API_BASE_URL:
        response = httpx.post(
            (
                f"{API_BASE_URL}"
                "/api/v1/trips/plan"
            ),
            json=payload,
            timeout=60.0,
        )

        response.raise_for_status()

        return response.json()

    trip_request = TripRequest(
        **payload
    )

    plan = plan_trip(
        trip_request
    )

    safe_plan = make_json_safe(
        plan
    )

    status = (
        "PLANNED_WITH_WARNINGS"
        if safe_plan.get("warnings")
        else "PLANNED"
    )

    return {
        "trip_id": "cloud-demo",
        "status": status,
        "plan": safe_plan,
    }


def format_money(
    amount: float | int | None,
    currency: str = "INR",
) -> str:
    if amount is None:
        return "N/A"

    return (
        f"{currency} "
        f"{float(amount):,.2f}"
    )


st.title(
    "✈️ TripPilot AI"
)

st.write(
    "Multi-Agent AI Travel Planner"
)

st.info(
    "Flights, stays and activities currently use "
    "demo/mock data. Weather and currency services "
    "use live providers when available."
)


with st.sidebar:
    st.header(
        "System"
    )

    if API_BASE_URL:
        st.success(
            "FastAPI Mode"
        )

        st.write(
            f"API: `{API_BASE_URL}`"
        )

        st.caption(
            "Streamlit is communicating with "
            "the FastAPI backend."
        )

    else:
        st.success(
            "Cloud Demo Mode"
        )

        st.write(
            "Backend: `Direct LangGraph`"
        )

        st.caption(
            "TripPilot planning logic is running "
            "directly inside Streamlit."
        )

    st.divider()

    st.caption(
        "TripPilot AI"
    )

    st.caption(
        "Python • LangGraph • FastAPI • "
        "Streamlit • Docker"
    )


with st.form(
    "trip_form",
):
    st.subheader(
        "Plan your trip"
    )

    col1, col2 = st.columns(2)

    with col1:
        origin = st.text_input(
            "Origin",
            value="Kolkata",
        )

        start_date = st.date_input(
            "Start date",
            value=(
                date.today()
                + timedelta(days=30)
            ),
        )

        travelers = st.number_input(
            "Travelers",
            min_value=1,
            max_value=20,
            value=2,
            step=1,
        )

    with col2:
        destination = st.text_input(
            "Destination",
            value="Goa",
        )

        end_date = st.date_input(
            "End date",
            value=(
                date.today()
                + timedelta(days=34)
            ),
        )

        budget = st.number_input(
            "Budget",
            min_value=1.0,
            value=30000.0,
            step=1000.0,
        )

    currency = st.selectbox(
        "Currency",
        options=[
            "INR",
            "USD",
            "EUR",
            "GBP",
        ],
        index=0,
    )

    preference_text = st.text_input(
        "Preferences",
        value="Beach, Food",
        help=(
            "Enter preferences separated "
            "by commas."
        ),
    )

    submitted = st.form_submit_button(
        "🚀 Plan My Trip",
        use_container_width=True,
    )


if submitted:
    preferences = [
        item.strip()
        for item
        in preference_text.split(",")
        if item.strip()
    ]

    payload = {
        "origin": origin,
        "destination": destination,
        "start_date": (
            start_date.isoformat()
        ),
        "end_date": (
            end_date.isoformat()
        ),
        "travelers": int(
            travelers
        ),
        "budget": float(
            budget
        ),
        "currency": currency,
        "preferences": preferences,
    }

    if start_date > end_date:
        st.error(
            "End date must be on or after "
            "the start date."
        )

    else:
        with st.spinner(
            "TripPilot agents are "
            "planning your trip..."
        ):
            try:
                result = call_trip_planner(
                    payload
                )

                st.session_state[
                    "trip_result"
                ] = result

            except httpx.HTTPStatusError as error:
                st.error(
                    "Trip planning request failed."
                )

                try:
                    st.json(
                        error.response.json()
                    )

                except Exception:
                    st.write(
                        error.response.text
                    )

            except httpx.RequestError:
                st.error(
                    "The FastAPI backend could not "
                    "be reached."
                )

                st.info(
                    "If you are running with Docker, "
                    "make sure the API container "
                    "is running."
                )

            except Exception as error:
                st.error(
                    "Trip planning could not "
                    "be completed."
                )

                st.caption(
                    f"Error type: "
                    f"{type(error).__name__}"
                )


result = st.session_state.get(
    "trip_result"
)


if result:
    trip_id = result.get(
        "trip_id"
    )

    status = result.get(
        "status",
        "UNKNOWN",
    )

    plan = result.get(
        "plan",
        {},
    )

    if trip_id == "cloud-demo":
        st.success(
            "Trip generated successfully."
        )

    else:
        st.success(
            f"Trip #{trip_id} "
            "created successfully."
        )

    if status == "PLANNED":
        st.success(
            "Status: PLANNED"
        )

    else:
        st.warning(
            f"Status: {status}"
        )

    request_data = plan.get(
        "request",
        {},
    )

    flights = plan.get(
        "flights",
        [],
    )

    stays = plan.get(
        "stays",
        [],
    )

    activities = plan.get(
        "activities",
        [],
    )

    weather = plan.get(
        "weather",
        {},
    )

    currency_data = plan.get(
        "currency_conversion",
        {},
    )

    budget_data = (
        plan.get("budget")
        or {}
    )

    itinerary = plan.get(
        "itinerary",
        [],
    )

    warnings = plan.get(
        "warnings",
        [],
    )

    errors = plan.get(
        "errors",
        [],
    )

    (
        overview_tab,
        travel_tab,
        weather_tab,
        itinerary_tab,
        diagnostics_tab,
    ) = st.tabs(
        [
            "Overview",
            "Travel Options",
            "Weather & Currency",
            "Itinerary",
            "Diagnostics",
        ]
    )

    with overview_tab:
        st.subheader(
            "Trip Overview"
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        with col1:
            st.metric(
                "Origin",
                request_data.get(
                    "origin",
                    origin,
                ),
            )

        with col2:
            st.metric(
                "Destination",
                request_data.get(
                    "destination",
                    destination,
                ),
            )

        with col3:
            st.metric(
                "Travelers",
                request_data.get(
                    "travelers",
                    travelers,
                ),
            )

        st.subheader(
            "Budget"
        )

        currency_code = (
            request_data.get(
                "currency",
                currency,
            )
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        with col1:
            st.metric(
                "Estimated Cost",
                format_money(
                    budget_data.get(
                        "total_cost"
                    ),
                    currency_code,
                ),
            )

        with col2:
            st.metric(
                "Budget",
                format_money(
                    budget_data.get(
                        "user_budget"
                    ),
                    currency_code,
                ),
            )

        with col3:
            st.metric(
                "Remaining",
                format_money(
                    budget_data.get(
                        "remaining_budget"
                    ),
                    currency_code,
                ),
            )

        st.write(
            "**Budget Status:**",
            budget_data.get(
                "status",
                "Unknown",
            ),
        )

    with travel_tab:
        st.subheader(
            "✈️ Flights"
        )

        if flights:
            st.dataframe(
                flights,
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Flight information currently "
                "uses demo/mock provider data."
            )

        else:
            st.warning(
                "No flight data available."
            )

        st.subheader(
            "🏨 Stays"
        )

        if stays:
            st.dataframe(
                stays,
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Stay information currently "
                "uses demo/mock provider data."
            )

        else:
            st.warning(
                "No stay data available."
            )

        st.subheader(
            "🏖️ Activities"
        )

        if activities:
            st.dataframe(
                activities,
                use_container_width=True,
                hide_index=True,
            )

            st.caption(
                "Activity information currently "
                "uses demo/mock provider data."
            )

        else:
            st.warning(
                "No activity data available."
            )

    with weather_tab:
        st.subheader(
            "🌤️ Live Weather"
        )

        if weather:
            col1, col2, col3 = (
                st.columns(3)
            )

            with col1:
                st.metric(
                    "Location",
                    weather.get(
                        "resolved_location",
                        "N/A",
                    ),
                )

            with col2:
                temperature = (
                    weather.get(
                        "temperature_c"
                    )
                )

                st.metric(
                    "Temperature",
                    (
                        f"{temperature} °C"
                        if temperature
                        is not None
                        else "N/A"
                    ),
                )

            with col3:
                feels_like = (
                    weather.get(
                        "feels_like_c"
                    )
                )

                st.metric(
                    "Feels Like",
                    (
                        f"{feels_like} °C"
                        if feels_like
                        is not None
                        else "N/A"
                    ),
                )

            col1, col2 = (
                st.columns(2)
            )

            with col1:
                st.metric(
                    "Precipitation",
                    (
                        f"{weather.get('precipitation_mm')} mm"
                        if weather.get(
                            "precipitation_mm"
                        )
                        is not None
                        else "N/A"
                    ),
                )

            with col2:
                st.metric(
                    "Wind Speed",
                    (
                        f"{weather.get('wind_speed_kmh')} km/h"
                        if weather.get(
                            "wind_speed_kmh"
                        )
                        is not None
                        else "N/A"
                    ),
                )

            st.caption(
                "Weather provider: "
                f"{weather.get('provider', 'Unknown')}"
            )

        else:
            st.warning(
                "Live weather is currently "
                "unavailable."
            )

        st.divider()

        st.subheader(
            "💱 Currency Conversion"
        )

        if currency_data:
            col1, col2 = (
                st.columns(2)
            )

            with col1:
                st.metric(
                    "Original Budget",
                    (
                        f"{currency_data.get('original_amount')} "
                        f"{currency_data.get('original_currency')}"
                    ),
                )

            with col2:
                st.metric(
                    "Converted Budget",
                    (
                        f"{currency_data.get('converted_amount')} "
                        f"{currency_data.get('converted_currency')}"
                    ),
                )

            st.write(
                "**Exchange rate:**",
                currency_data.get(
                    "rate",
                    "N/A",
                ),
            )

            st.caption(
                "Currency provider: "
                f"{currency_data.get('provider', 'Unknown')}"
            )

        else:
            st.warning(
                "Currency conversion is "
                "currently unavailable."
            )

    with itinerary_tab:
        st.subheader(
            "🗓️ Suggested Itinerary"
        )

        if itinerary:
            for day_data in itinerary:
                day_number = (
                    day_data.get(
                        "day",
                        "",
                    )
                )

                day_date = (
                    day_data.get(
                        "date",
                        "",
                    )
                )

                hotel = (
                    day_data.get(
                        "hotel"
                    )
                )

                day_activities = (
                    day_data.get(
                        "activities",
                        [],
                    )
                )

                with st.container(
                    border=True
                ):
                    st.markdown(
                        f"### Day {day_number}"
                    )

                    if day_date:
                        st.caption(
                            day_date
                        )

                    if hotel:
                        st.write(
                            f"🏨 **Hotel:** "
                            f"{hotel}"
                        )

                    for activity in (
                        day_activities
                    ):
                        st.write(
                            f"• {activity}"
                        )

        else:
            st.warning(
                "No itinerary available."
            )

    with diagnostics_tab:
        st.subheader(
            "System Diagnostics"
        )

        if API_BASE_URL:
            st.info(
                "Execution mode: "
                "FastAPI backend"
            )

        else:
            st.info(
                "Execution mode: "
                "Direct Streamlit Cloud"
            )

        st.subheader(
            "Warnings"
        )

        if warnings:
            for warning in warnings:
                st.warning(
                    warning
                )

        else:
            st.success(
                "No warnings."
            )

        st.subheader(
            "Agent Errors"
        )

        if errors:
            st.warning(
                "Some optional providers "
                "reported errors."
            )

            st.json(
                errors
            )

        else:
            st.success(
                "No agent errors."
            )

        with st.expander(
            "Raw Plan Data"
        ):
            st.json(
                plan
            )


st.divider()

st.caption(
    "TripPilot AI is an educational and portfolio project. "
    "Demo flight, stay and activity information should not "
    "be treated as live booking availability."
)