from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from gargula.settings import settings

def register_cors_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.cors_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
