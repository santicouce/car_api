from dotenv import load_dotenv

load_dotenv("env/test.env")
from fastapi import FastAPI
from routers import cars, drivers, auth


app = FastAPI()

app.include_router(cars.router)
app.include_router(drivers.router)
app.include_router(auth.router)
