from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.auth  import router as auth_router
from app.api.crud.category import router as category_crud_router


router = APIRouter()

router.include_router(health_router)
router.include_router(auth_router)
router.include_router(category_crud_router)