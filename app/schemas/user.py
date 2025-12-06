from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=72)


class UserRead(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
