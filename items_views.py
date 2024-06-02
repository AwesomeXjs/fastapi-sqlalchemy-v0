from typing import Annotated

from fastapi import APIRouter, Path

router = APIRouter(prefix="/items")


@router.get("/items/")
def get_items():
    return ["items"]


@router.get("/items/latest")
def get_latest_items():
    return ["items"]


@router.get("/items/{item_id}")
def get_item_by_id(item_id: Annotated[int, Path(ge=1, lt=100)]):
    return f"Тут айтем с айди {item_id}"
