from typing import Annotated

import uvicorn
from fastapi import FastAPI, Path
from pydantic import EmailStr, BaseModel

from items_views import router as items_router

app = FastAPI(title="Suren App")
app.include_router(items_router)


class CreateUser(BaseModel):
    email: EmailStr


@app.get("/")
def get_home():
    return {"message": "hello world"}


@app.get("/hello/")
def get_hello(name: str):
    name = name.strip().title()
    return f"hello from {name}"


@app.post("/users/")
def add_user(user: CreateUser):
    return {"message": "success", "email": user.email}


@app.post("/users/{user_id}")
def change_name_user(user_id: int, new_name: str):
    return f"Имя пользователя с айди {user_id} изменено на {new_name}"


@app.get("/teachers")
def get_teachers(offset: int = 0, limit: int = 1):
    all_teachers = [1, 34, 67, 8, 3]
    return all_teachers[offset:][:limit]


class NumberForSum(BaseModel):
    first_num: int
    second_num: int


@app.post("/sum")
def summary(numbers: NumberForSum):
    return {
        "first_num": numbers.first_num,
        "second_num": numbers.second_num,
        "summary": numbers.first_num + numbers.second_num,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
