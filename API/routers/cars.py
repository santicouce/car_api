import models
from database import SessionLocal, engine
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from routers.auth import get_current_user, get_user_exception


router = APIRouter(prefix="/cars", tags=["cars"])

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


class Car(BaseModel):
    """Car's base model.
    """
    plate: str = Field(description="Cars's plate. Should be a valid Mercosur plate type.", min_length=6)
    color: str
    chassis: str = Field(description="Cars's chassis.", min_length=1)
    doors_quantity: int = Field(description="Cars's doors quantity. Should be grather than 1.", gt=1)
    insured: bool = Field(True, description="Indicates if car is insured or not. Default is True.")

    # Example for docs.
    class Config:
        schema_extra = {"example": {"plate": "abc123", "color": "Green", "chassis": "526a48skq0a", "doors_quantity": 4,"insured":True}}

@router.get("/")
def get_all_cars(db : Session = Depends(get_db), user: dict = Depends(get_current_user)):
    """Get information from all cars recorded.
    """
    if not user:
        raise get_user_exception()

    return db.query(models.Cars).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_new_car(car: Car, db: Session = Depends(get_db)):
    """Register new car.
    """
    car_model = models.Cars()
    car_model.plate = car.plate
    car_model.color = car.color
    car_model.chassis = car.chassis
    car_model.doors_quantity = car.doors_quantity
    car_model.insured = car.insured
    db.add(car_model)
    db.commit()
    return {"description": "Car added."}


@router.delete("/delete/")
def delete_car(car_plate: str, db: Session = Depends(get_db)):
    """Delete a car.
    """
    car_model = db.query(models.Cars)\
        .filter(models.Cars.plate == car_plate)\
        .first()

    if car_model is None:
        raise http_exception()

    db.query(models.Cars)\
        .filter(models.Cars.plate == car_plate)\
        .delete()

    db.commit()
    return {"status_code": 200, "description": "Car deleted."}



@router.get("/search/")
def get_car(car_plate: str, db: Session = Depends(get_db)):
    """Search car by plate.
    Args:
        car_plate (str): car's plate.
    """
    car_model = db.query(models.Cars)\
        .filter(models.Cars.plate == car_plate)\
        .first()
    if car_model is not None:
        return car_model
    raise http_exception()

def http_exception():
    """Raise exception for car now found.
    """
    return HTTPException(status_code=404, detail="Car not found")
