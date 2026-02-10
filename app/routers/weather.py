from fastapi import APIRouter, HTTPException
from app.services.weather import get_weather
from app.schemas.weather import WeatherResponse

router = APIRouter()

@router.get("/{city}", response_model=WeatherResponse)
async def read_weather(city: str):
    try:
        data = await get_weather(city)
        weather_data = WeatherResponse(
            city=data["name"],
            weather=data["weather"][0]["main"],
            description=data["weather"][0]["description"],
            main=data["main"]
        )
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
