from fastapi import FastAPI
from gargula.exceptions import register_exception_handlers
from gargula.middlewares import register_middlewares
from gargula.routes import register_routes

app = FastAPI(title="Gargula API")

register_middlewares(app)
register_exception_handlers(app)
register_routes(app)
