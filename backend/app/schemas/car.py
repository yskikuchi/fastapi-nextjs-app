from pydantic import BaseModel, UUID4, ConfigDict


class CarBase(BaseModel):
    pass


class CarCreate(CarBase):
    name: str
    capacity: int
    car_number: str


class CarCreateResponse(CarBase):
    pass


class Car(CarBase):
    id: UUID4
    name: str
    capacity: int
    car_number: str
    model_config = ConfigDict(form_attribure=True)
