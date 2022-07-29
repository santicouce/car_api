from typing import Optional
from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel, Field

DRIVERS = []
router = APIRouter(prefix="/drivers", tags=["drivers"])


class Driver(BaseModel):
    name: str = Field(description="Driver's name.", min_length=1)
    age: int = Field(description="Driver's age. Should be grather than 16.", gt=15)
    id: int
    car_plate: Optional[str] = Field(description="Cars's plate. Should be a valid Mercosur plate type,", min_length=6)

    # Example
    class Config:
        schema_extra = {"example": {"name": "Santiago", "age": 25, "id": 34682222, "car_plate": "abc123"}}


@router.get("/")
def get_all_drivers():
    return DRIVERS


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_new_driver(driver: Driver):
    """Add a driver."""
    DRIVERS.append(driver)
    return {"description": "Driver added."}


@router.get("/search/")
def get_driver(driver_id: int):
    """Search driver by plate."""
    for driver in DRIVERS:
        if driver.id == driver_id:
            return driver
    raise HTTPException(status_code=404, detail="Driver not found.")
