from pydantic import BaseModel, EmailStr, ConfigDict
from pydantic.alias_generators import to_camel


class AdminBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class AdminCreate(AdminBase):
    name: str
    email: EmailStr
    password: str
