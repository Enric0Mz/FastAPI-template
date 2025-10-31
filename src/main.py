from fastapi import FastAPI

from starlette.middleware.sessions import SessionMiddleware
from src.routes.health import router as health_router
from src.routes.users import router as users_router
from src.routes.sessions import router as sessions_router
from src.routes.google import router as google_router


app = FastAPI(
    title="FastAPI Project Template (modify this)",
    description="This project has the goal of beeing a template for other FastAPI Projects that use PosgreSQL.",
    version="0.1.0",
)

app.add_middleware(
    SessionMiddleware,
    secret_key="z1d3be5c4acc063892cc97744c32733acdf1d98f11088744031dd561f2924135f1",
)


app.include_router(health_router)
app.include_router(users_router)
app.include_router(sessions_router)
app.include_router(google_router)
