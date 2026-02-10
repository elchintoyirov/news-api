from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import bauth, users, news, weather

app = FastAPI(title="News API (Beta)", version="1.0")

app.include_router(bauth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(weather.router, prefix="/weather", tags=["Weather"])

@app.get("/")
def root():
    return RedirectResponse(url="/docs")