from typing import Optional
from sqlalchemy.exc import IntegrityError
import models
from database import SessionLocal, engine
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from requests import Session

router = APIRouter(prefix="/drivers", tags=["drivers"])

#Create tables if not present on db.
models.Base.metadata.create_all(bind=engine)


def get_db():
    """Get session for data base.

    Yields:
        SessionLocal: session for data base.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Driver(BaseModel):
    """Driver's base model.
    """
    name: str = Field(description="Driver's name.", min_length=1)
    age: int = Field(description="Driver's age. Should be grather than 16.", gt=15)
    id: int
    car_plate: Optional[str] = Field(description="Cars's plate. Should be a valid Mercosur plate type.", min_length=6)

    # Example for docs.
    class Config:
        schema_extra = {"example": {"name": "Santiago", "age": 25, "id": 34682222, "car_plate": "abc123"}}


@router.get("/")
def get_all_drivers(db : Session = Depends(get_db)):
    """Get all drivers.
    """
    return db.query(models.Drivers).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_new_driver(driver: Driver, db: Session = Depends(get_db)):
    """Add a driver."""
    driver_model = models.Drivers()
    driver_model.name = driver.name
    driver_model.age = driver.age
    driver_model.id = driver.id
    driver_model.car_plate = driver.car_plate
    try:
        db.add(driver_model)
        db.commit()
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Driver not added. Relational integrity of the database is affected.')

    return {"status_code": 200, "description": "Driver added."}


@router.get("/search/")
def get_driver(driver_id: int,  db: Session = Depends(get_db)):
    """Search driver by id."""
    
    driver_model = db.query(models.Drivers).filter(models.Drivers.id == driver_id).first()

    if not driver_model:
        raise HTTPException(status_code=404, detail="Driver not found.")

    return driver_model
