from fastapi import FastAPI, APIRouter
from gargula.routes import lesson_route, subject_route

def register_routes(app: FastAPI) -> None:
    v1_router = APIRouter(prefix="/v1")
    v1_router.include_router(lesson_route.router, prefix="/lessons")
    v1_router.include_router(subject_route.router, prefix="/subjects")
    app.include_router(v1_router)
