import httpx

from app.config import settings


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


WEATHER_LOCATION_ALIASES = {
    "goa": "Panjim, Goa",
}


def normalize_weather_location(location: str) -> str:
    cleaned = location.strip()

    return WEATHER_LOCATION_ALIASES.get(
        cleaned.casefold(),
        cleaned,
    )


def _split_location(
    location: str,
) -> tuple[str, str | None]:

    parts = [
        part.strip()
        for part in location.split(",")
        if part.strip()
    ]

    city = parts[0]

    admin1 = None

    if len(parts) >= 2:
        admin1 = parts[1]

    return city, admin1


def _choose_best_location(
    city: str,
    results: list[dict],
    admin1: str | None = None,
) -> dict:

    city_lower = city.casefold()

    exact_name_matches = [
        result
        for result in results
        if result.get("name", "").casefold()
        == city_lower
    ]

    candidates = exact_name_matches or results

    if admin1:
        admin_lower = admin1.casefold()

        admin_matches = [
            result
            for result in candidates
            if result.get("admin1", "").casefold()
            == admin_lower
        ]

        if admin_matches:
            candidates = admin_matches
        else:
            raise ValueError(
                f"Could not find {city} in {admin1}."
            )

    city_codes = {
        "PPLC",
        "PPLA",
        "PPLA2",
        "PPLA3",
        "PPLA4",
        "PPL",
    }

    city_matches = [
        result
        for result in candidates
        if result.get("feature_code") in city_codes
    ]

    if city_matches:
        return max(
            city_matches,
            key=lambda item: item.get(
                "population",
                0,
            ) or 0,
        )

    return candidates[0]


def get_coordinates(
    location: str,
    country_code: str = "IN",
) -> dict:

    location = normalize_weather_location(
        location
    )

    city, admin1 = _split_location(
        location
    )

    response = httpx.get(
        GEOCODING_URL,
        params={
            "name": city,
            "count": 100,
            "language": "en",
            "format": "json",
            "countryCode": country_code,
        },
        timeout=settings.request_timeout,
    )

    response.raise_for_status()

    data = response.json()

    results = data.get(
        "results",
        [],
    )

    if not results:
        raise ValueError(
            f"Could not find {city} "
            f"in country {country_code}."
        )

    best_match = _choose_best_location(
        city=city,
        results=results,
        admin1=admin1,
    )

    return {
        "name": best_match.get("name"),
        "latitude": best_match["latitude"],
        "longitude": best_match["longitude"],
        "country": best_match.get("country"),
        "country_code": best_match.get(
            "country_code"
        ),
        "admin1": best_match.get("admin1"),
        "feature_code": best_match.get(
            "feature_code"
        ),
    }


def get_weather(
    location: str,
    country_code: str = "IN",
) -> dict:

    normalized_location = (
        normalize_weather_location(
            location
        )
    )

    place = get_coordinates(
        normalized_location,
        country_code,
    )

    response = httpx.get(
        WEATHER_URL,
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": (
                "temperature_2m,"
                "apparent_temperature,"
                "precipitation,"
                "weather_code,"
                "wind_speed_10m"
            ),
            "timezone": "auto",
        },
        timeout=settings.request_timeout,
    )

    response.raise_for_status()

    data = response.json()

    current = data.get("current")

    if not current:
        raise ValueError(
            f"Weather data unavailable "
            f"for {location}."
        )

    return {
        "requested_location": location,
        "normalized_location": (
            normalized_location
        ),
        "resolved_location": place["name"],
        "admin1": place["admin1"],
        "country": place["country"],
        "country_code": country_code,
        "feature_code": (
            place["feature_code"]
        ),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "temperature_c": current.get(
            "temperature_2m"
        ),
        "feels_like_c": current.get(
            "apparent_temperature"
        ),
        "precipitation_mm": current.get(
            "precipitation"
        ),
        "weather_code": current.get(
            "weather_code"
        ),
        "wind_speed_kmh": current.get(
            "wind_speed_10m"
        ),
        "provider": "open_meteo",
        "source_type": "live",
    }