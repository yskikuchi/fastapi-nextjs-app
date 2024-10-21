from pydantic import BaseModel, UUID4, ConfigDict
from pydantic.alias_generators import to_camel


class CarBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


class CarCreate(CarBase):
    name: str
    capacity: int
    car_number: str
    price_for_initial_twelve_hours: int
    price_per_additional_six_hours: int


class CarCreateResponse(CarBase):
    pass


class CarUpdate(CarBase):
    name: str
    capacity: int
    car_number: str
    price_for_initial_twelve_hours: int
    price_per_additional_six_hours: int


class Car(CarBase):
    id: UUID4
    name: str
    capacity: int
    car_number: str
    price_for_initial_twelve_hours: int
    price_per_additional_six_hours: int
    model_config = ConfigDict(form_attribure=True)
