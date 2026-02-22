from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import auth_router, users_router, news_router, weather_router
from app.admin.settings import admin

app = FastAPI(title="News API (Beta)", version="1.0")
admin.mount_to(app)

app.include_router(auth_router, tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(news_router, prefix="/news", tags=["News"])
app.include_router(weather_router, prefix="/weather", tags=["Weather"])


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
