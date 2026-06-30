from fastapi import FastAPI
from app.api.router import router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Lead Management System Backend",
    version=settings.app_version,
)

app.include_router(router)