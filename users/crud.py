# create read update delete

from users.schemas import CreateUser


def create_user(user_in: CreateUser) -> dict:
    user = user_in.model_dump()
    return {"success": True, "user": user}


def upgrade_name(user_id: int, new_name: str):
    return f"Имя пользователя с айди {user_id} изменено на {new_name}"
