from fastapi import FastAPI
from app.api.routes import rides, shifts, health
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(title="Driver Analytics API")

app.include_router(health.router)
app.include_router(rides.router, prefix="/rides")
app.include_router(shifts.router, prefix="/shifts")
