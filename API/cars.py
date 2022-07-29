from fastapi import FastAPI
from pydantic import BaseModel

CARS = []
app = FastAPI()


class Car(BaseModel):
    plate: str
    color: str
    chassis: str
    doors_quantity: int
    insured: bool


@app.get("/")
def get_all_cars():
    return CARS


@app.post("/")
def add_new_car(car: Car):
    CARS.append(car)
    return {"status_code": 200, "description": "Car added."}


@app.get("/search/")
def get_car(car_plate):
    for car in CARS:
        if car.plate == car_plate:
            return car
    return {"status_code": 404, "description": "Car not found."}
