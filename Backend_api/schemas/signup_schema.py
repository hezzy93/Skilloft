from pydantic import BaseModel, ConfigDict
from uuid import UUID

class UserBase(BaseModel):
    last_name: str
    first_name: str
    email: str
    

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)