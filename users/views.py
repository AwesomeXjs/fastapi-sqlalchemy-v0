from typing import Annotated
from annotated_types import MinLen, MaxLen

from fastapi import APIRouter

from users.schemas import CreateUser
from users import crud

router = APIRouter(prefix="/users")


@router.post("/")
def add_user(user: CreateUser):
    return crud.create_user(user)


@router.post("/{user_id}")
def change_name_user(user_id: int, new_name: Annotated[str, MinLen(2), MaxLen(20)]):
    return crud.change_name(user_id=user_id, new_name=new_name)
