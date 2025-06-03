from fastapi import APIRouter

from src.api.routers import auth, crm, tested_users, tests, users


router = APIRouter(prefix="/api_v1")
router.include_router(crm.router)
router.include_router(tests.router)
router.include_router(users.router)
router.include_router(tested_users.router)
router.include_router(auth.router)
