import random
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, value, key='sticky'):
        super().__init__(app)
        self.value = value
        self.key = key

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.set_cookie(key=self.key, value=self.value)
        return response


server_name = f"st-{random.random()}"


def init_shiny(app):
    app.starlette_app.user_middleware.append(
        Middleware(CustomHeaderMiddleware, value=server_name, key="sticky")
    )