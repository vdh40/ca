from fastapi import APIRouter

from .routers import courses, currencies

router = APIRouter()

router.include_router(courses.router, tags=["courses"])
router.include_router(currencies.router, tags=["currencies"])
