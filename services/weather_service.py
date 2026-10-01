import requests
from typing import Optional

def fetch_weather_forecast(
    city: Optional[str] = None, 
    latitude: Optional[float] = None, 
    longitude: Optional[float] = None
) -> dict:
    """
    Fetches real-time weather.
    If no coordinates provided, defaults to Tbilisi (41.7151, 44.8271).
    """
    lat, lon = latitude, longitude

    # 1. თუ გადაეცა ქალაქის სახელი, ამოვიღოთ კოორდინატები Geocoding-ით
    if city and (lat is None or lon is None):
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
            geo_res = requests.get(geo_url, timeout=5).json()
            if geo_res.get("results"):
                lat = geo_res["results"][0]["latitude"]
                lon = geo_res["results"][0]["longitude"]
        except Exception:
            pass

    # 2. Default Fallback (თუ კოორდინატები არ მოვიდა, გამოიყენე თბილისი)
    if lat is None or lon is None:
        lat, lon = 41.7151, 44.8271

    # 3. ამინდის გამოთხოვა
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            current = response.json().get("current_weather", {})
            return {
                "location": city or f"{lat}, {lon}",
                "temperature": current.get("temperature"),
                "windspeed": current.get("windspeed"),
                "weather_code": current.get("weathercode"),
                "is_day": current.get("is_day")
            }
        return {"error": "Weather service unavailable."}
    except Exception as e:
        return {"error": f"Failed to fetch weather: {str(e)}"}