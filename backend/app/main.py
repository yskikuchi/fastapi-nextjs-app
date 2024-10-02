from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.routers import booking, car, admin

app = FastAPI()

app.include_router(booking.router)
app.include_router(car.router)
app.include_router(admin.router)
