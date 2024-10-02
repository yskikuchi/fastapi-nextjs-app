from pydantic import BaseModel, EmailStr


class AdminBase(BaseModel):
    pass


class AdminCreate(AdminBase):
    name: str
    email: EmailStr
    password: str
