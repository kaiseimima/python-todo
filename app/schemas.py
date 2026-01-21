from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional

class TodoBase(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    completed: bool = False

class TodoCreate(TodoBase):
    pass

class TodoSchema(TodoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr # email-validator が自動で形式チェックしてくれます

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

