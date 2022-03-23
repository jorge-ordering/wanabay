from re import A
from fastapi import FastAPI

from app.api.api import api_router

app = FastAPI(title="Wanna Bay")

app.include_router(api_router)
