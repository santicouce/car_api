from fastapi import APIRouter
from pydantic import BaseModel

CARS = []
router = APIRouter(prefix="/cars", tags=["cars"])


class Car(BaseModel):
    plate: str
    color: str
    chassis: str
    doors_quantity: int
    insured: bool


@router.get("/")
def get_all_cars():
    return CARS


@router.post("/")
def add_new_car(car: Car):
    CARS.append(car)
    return {"status_code": 200, "description": "Car added."}


@router.delete("/delete/")
def delete_car(car_plate: str):
    for car in CARS:
        if car.plate == car_plate:
            CARS.remove(car)
            return {"status_code": 200, "description": "Car deleted."}
    return {"status_code": 404, "description": "Car not found."}


@router.get("/search/")
def get_car(car_plate: str):
    """Search car by plate.
    Args:
        car_plate (str): car's plate.
    """
    for car in CARS:
        if car.plate == car_plate:
            return car
    return {"status_code": 404, "description": "Car not found."}
