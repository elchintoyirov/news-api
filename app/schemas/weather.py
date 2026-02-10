from pydantic import BaseModel

class WeatherMain(BaseModel):
    temp: float
    feels_like: float
    humidity: int

class WeatherResponse(BaseModel):
    city: str
    weather: str
    description: str
    main: WeatherMain
