from sqlalchemy import Boolean, Column, Integer, String

from database import Base


class Users(Base):
    """Base for users table."""

    __tablename__ = "users"

    username = Column(String(50), primary_key=True, index=True)
    email = Column(String(50))
    first_name = Column(String(50))
    last_name = Column(String(50))
    hashed_password = Column(String(200))


class Drivers(Base):
    """Base for drivers table."""

    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    age = Column(Integer)
    car_plate = Column(String(7))


class Cars(Base):
    """Base for cars table."""

    __tablename__ = "cars"

    plate = Column(String(7), primary_key=True, index=True)
    color = Column(String(14))
    chassis = Column(String(14))
    doors_quantity = Column(Integer)
    insured = Column(Boolean, default=True)
