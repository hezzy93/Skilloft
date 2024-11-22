from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional

class UserBase(BaseModel):
    last_name: Optional[str] = None  # Make last_name optional
    first_name: Optional[str] = None  # Make last_name optional
    email: str
    

class UserCreate(BaseModel):
    email: str
    password: str

class User(UserBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)