from pydantic import BaseModel, ConfigDict, Field
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