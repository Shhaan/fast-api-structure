from pydantic import BaseModel
from fastapi import Form
from typing import Optional
class LoginSchema(BaseModel):
    email: str
    password: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        password: str = Form(...)
    ):
        return cls(email=email, password=password)
    

class UserSchema(BaseModel):
    email: str
    name: Optional[str] = None
    password: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
         name: Optional[str] = Form(None), 
        password: str = Form(...)
    ):
        return cls(email=email, name=name, password=password)