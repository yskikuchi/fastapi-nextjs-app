from pydantic import BaseModel, UUID4, ConfigDict


class CarBase(BaseModel):
    pass


class CarCreate(CarBase):
    name: str
    capacity: int
    car_number: str
    price_for_initial_twelve_hours: int
    price_per_additional_six_hours: int


class CarCreateResponse(CarBase):
    pass


class Car(CarBase):
    id: UUID4
    name: str
    capacity: int
    car_number: str
    price_for_initial_twelve_hours: int
    price_per_additional_six_hours: int
    model_config = ConfigDict(form_attribure=True)
