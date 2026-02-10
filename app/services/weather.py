import httpx
from app.config import OPENWEATHER_API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_weather(city: str, units: str = "metric"):
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": units
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(BASE_URL, params=params)
        resp.raise_for_status()
        return resp.json()