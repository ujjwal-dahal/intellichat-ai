import httpx
from datetime import datetime
from zoneinfo import ZoneInfo
from langchain.tools import tool


@tool
def weather_tool(
    location: str,
    forecast_days: int = 1
) -> dict:
    """Get current weather and daily forecast for a given location."""

    if not 1 <= forecast_days <= 16:
        raise ValueError("forecast_days must be between 1 and 16.")

    # Step 1: Extract latitude and longitude
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    query_parameters_1 = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    response_1 = httpx.get(
        url=geocoding_url,
        params=query_parameters_1,
        timeout=10,
    )
    response_1.raise_for_status()

    result_1 = response_1.json()
    
    locations = result_1.get("results", [])

    if not locations:
        return {"error": f"Location '{location}' not found."}

    location_data = locations[0]

    latitude = location_data["latitude"]
    longitude = location_data["longitude"]


    # Step 2: Extract weather forecast
    weather_url = "https://api.open-meteo.com/v1/forecast"


    query_parameters_2 = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "wind_speed_10m"
        ),
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "sunrise,"
            "sunset"
        ),
        "forecast_days": forecast_days,
        "timezone": "Asia/Kathmandu",
    }

    response_2 = httpx.get(
        url=weather_url,
        params=query_parameters_2,
        timeout=10,
    )
    response_2.raise_for_status()

    weather_result = response_2.json()

    # Step 3: Extract current weather
    current = weather_result["current"]
    current_units = weather_result["current_units"]

    current_weather_result = {
        "temperature": (
            f"{current['temperature_2m']} "
            f"{current_units['temperature_2m']}"
        ),
        "humidity": (
            f"{current['relative_humidity_2m']} "
            f"{current_units['relative_humidity_2m']}"
        ),
        "wind_speed": (
            f"{current['wind_speed_10m']} "
            f"{current_units['wind_speed_10m']}"
        ),
    }

    # Step 4: Extract daily forecast
    daily = weather_result["daily"]
    daily_units = weather_result["daily_units"]

    multiple_days_weather = {
    "dates": daily["time"],

    "temperature_2m_max": {
        "values": daily["temperature_2m_max"],
        "unit": daily_units["temperature_2m_max"],
    },

    "temperature_2m_min": {
        "values": daily["temperature_2m_min"],
        "unit": daily_units["temperature_2m_min"],
    },

    "sunrise": daily["sunrise"],
    "sunset": daily["sunset"],
}
    

    # Step 5: Return the final result
    return {
        "location": location_data["name"],
        "country": location_data.get("country"),
        
        "current_date": datetime.now(
            ZoneInfo("Asia/Kathmandu")
        ).strftime("%Y-%m-%d"),
        
        "current_weather": current_weather_result,
        
        "daily_forecast": multiple_days_weather,
    }