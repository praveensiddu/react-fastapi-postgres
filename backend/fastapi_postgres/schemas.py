from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    full_name: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: str = None
    full_name: str = None

class UserOut(UserBase):
    id: int
    class Config:
        from_attributes = True
