from typing import Annotated

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.api.deps import SessionDep
from src.api.utils import Authorization
from src.requset_forms import OAuth2EmailRequestForm


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/login")
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2EmailRequestForm, Depends()],
    response: Response,
):
    await Authorization.login(session, form_data, response)
    return {"message": "Logged is successfully"}


@router.get("/logout")
def logout(response: Response):
    response.delete_cookie("token")
    return {"message": "Successfully logged out"}
