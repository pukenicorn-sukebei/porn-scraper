import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api import api_router

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(levelname)s][%(name)s] %(message)s',
)

app = FastAPI()

# CORS
origins = []

# Set all CORS enabled origins
# if config.BACKEND_CORS_ORIGINS:
#     origins_raw = config.BACKEND_CORS_ORIGINS.split(",")
#     for origin in origins_raw:
#         use_origin = origin.strip()
#         origins.append(use_origin)
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=origins,
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     ),

app.include_router(api_router)
