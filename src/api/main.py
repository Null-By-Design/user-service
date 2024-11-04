from fastapi import FastAPI
from src.api.controller import health_controller, user_controller

app = FastAPI()

app.include_router(health_controller.router)
app.include_router(user_controller.router)
