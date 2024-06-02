from typing import Annotated
from annotated_types import MaxLen, MinLen

from fastapi import Path
from pydantic import EmailStr, BaseModel, Field


class CreateUser(BaseModel):
    username: Annotated[str, MaxLen(20), MinLen(2)]
    # username: str = Field(max_length=10)
    email: EmailStr
