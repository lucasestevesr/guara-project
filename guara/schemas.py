from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from guara.models import TodoState


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(
        from_attributes=True
    )  # For Pydantic v2 compatibility


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 100


class TodoSchema(BaseModel):
    title: str
    description: str
    state: TodoState


class TodoPublic(TodoSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class TodoList(BaseModel):
    todos: list[TodoPublic]


class FilterTodo(FilterPage):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    state: TodoState | None = None
