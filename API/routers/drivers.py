from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

DRIVERS = []
router = APIRouter(prefix="/drivers", tags=["drivers"], responses={404: {"description": "Not found"}})


class Driver(BaseModel):
    name: str
    age: int
    id: int
    car_plate: Optional[str]


@router.get("/")
def get_all_drivers():
    return DRIVERS


@router.post("/")
def add_new_driver(driver: Driver):
    DRIVERS.append(driver)
    return {"status_code": 200, "description": "Driver added."}


@router.get("/search/")
def get_driver(driver_id: int):
    """Search driver by plate.
    Args:
        driver_plate (str): driver's plate.
    """
    for driver in DRIVERS:
        if driver.id == driver_id:
            return driver
    return {"status_code": 404, "description": "Driver not found."}
