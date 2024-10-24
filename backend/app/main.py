from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from app.routers import booking, car, admin
import json

app = FastAPI()


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(booking.router)
app.include_router(car.router)
app.include_router(admin.router)

with open("openapi.json", "w") as file:
    api_spec = app.openapi()
    file.write(json.dumps(api_spec))
