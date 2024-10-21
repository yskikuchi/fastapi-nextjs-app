from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic.alias_generators import to_camel


class UserBase(BaseModel):
    name: str
    email: EmailStr

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class UserCreate(UserBase):
    pass
