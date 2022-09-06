from fastapi import APIRouter

from .endpoints import jav

api_router = APIRouter()

api_router.include_router(jav.router, prefix='/jav', tags=["jav"])
