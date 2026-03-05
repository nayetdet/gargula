from fastapi import FastAPI
from gargula.exceptions import register_exception_handlers
from gargula.routes import register_routes

app = FastAPI(title="Gargula API")

register_exception_handlers(app)
register_routes(app)
