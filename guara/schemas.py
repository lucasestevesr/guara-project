from pydantic import BaseModel, ConfigDict, EmailStr


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
