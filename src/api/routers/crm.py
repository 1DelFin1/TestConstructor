from fastapi import APIRouter

from src.api.deps import SessionDep
from src.crud import crm_crud


router = APIRouter(
    prefix="/crm",
    tags=["crm"],
)


@router.get("/get_data")
async def get_data(session: SessionDep, test_id: int, email: str):
    result = await crm_crud.get_user_result(session, test_id, email)
    return result
