from datetime import datetime, timedelta
from typing import Optional

import models
from database import SessionLocal, engine
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os

router = APIRouter(prefix="/auth", tags=["auth"])

# Auth configurations
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

# Create tables if not present on db.
models.Base.metadata.create_all(bind=engine)


def get_db():
    """Get session for data base.

    Yields:
        sessionmaker: session for data base.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class User(BaseModel):
    """Define base model for a user."""

    username: str
    email: Optional[str]
    first_name: str
    last_name: str
    password: str


@router.post("/create/user")
async def create_new_user(user: User, db: Session = Depends(get_db)):
    """Create new user to access API methods."""
    user_model = models.Users()
    user_model.email = user.email
    user_model.username = user.username
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    hash_password = get_password_hash(user.password)
    user_model.hashed_password = hash_password
    db.add(user_model)
    db.commit()

    return {"description": "User created."}


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Get token for given user."""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, expires_delta=token_expires)
    return {"token": token}


def get_password_hash(password):
    """Hash given password."""
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    """Verify if password is correct."""
    return bcrypt_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db):
    """Authenticate user."""
    user = db.query(models.Users).filter(models.Users.username == username).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, expires_delta: Optional[timedelta] = None):
    """Create access token with given data."""
    encode = {"sub": username}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_bearer)):
    """Get user from given token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise get_user_exception()
        return {"username": username}
    except JWTError:
        raise get_user_exception()


# Exceptions
def get_user_exception():
    """Exception for invalid user authentication."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def token_exception():
    """Exception for invalid token."""
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response
