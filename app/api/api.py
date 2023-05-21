from fastapi import APIRouter

from .custom import LoggingRoute
from .endpoints import jav

api_router = APIRouter(route_class=LoggingRoute)

api_router.include_router(
    jav.router,
    prefix='/lookup',
    tags=["lookup"]
)
