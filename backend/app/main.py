from fastapi import FastAPI
from app.routers import booking, car

app = FastAPI()

app.include_router(booking.router)
app.include_router(car.router)
