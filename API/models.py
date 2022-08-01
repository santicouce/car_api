from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Drivers(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    car_plate = Column(String)


class Cars(Base):
    __tablename__ = "cars"

    plate = Column(String, primary_key=True, index=True)
    color = Column(String)
    chassis = Column(String)
    doors_quantity = Column(Integer)
    insured = Column(Boolean, default=True)
