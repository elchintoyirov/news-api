from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from app.routers import auth_router, users_router, news_router, weather_router
from app.admin.settings import admin
from app.middleware.request_time import request_time_middleware

app = FastAPI(title="News API (Beta)", version="1.0")
admin.mount_to(app)

app.include_router(auth_router, tags=["Auth"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(news_router, prefix="/news", tags=["News"])
app.include_router(weather_router, prefix="/weather", tags=["Weather"])


@app.get("/")
def root():
    return RedirectResponse(url="/docs")

@app.middleware("http")
async def add_request_time(request: Request, call_next):
    return await request_time_middleware(request, call_next)