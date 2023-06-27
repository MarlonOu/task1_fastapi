from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str
    password: str
    token: str
    age: int
    sex: str


class UserRequest(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
