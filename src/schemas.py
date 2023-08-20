from pydantic import BaseModel, EmailStr, Field
from datetime  import date,datetime



class UserSchema(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str

    class Config:
        from_attributes  = True




class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactModel(BaseModel):
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday:date
    notes:str


class ContactResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday:date
    notes:str

    class Config:
        orm_mode = True


