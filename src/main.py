from fastapi import FastAPI

from src.routes.health import router as health_router
from src.routes.users import router as users_router
from src.routes.sessions import router as sessions_router


app = FastAPI(
    title="FastAPI Project Template (modify this)",
    description="This project has the goal of beeing a template for other FastAPI Projects that use PosgreSQL.",
    version="0.1.0",
)


app.include_router(health_router)
app.include_router(users_router)
app.include_router(sessions_router)
