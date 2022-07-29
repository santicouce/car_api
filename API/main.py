from fastapi import FastAPI
from routers import drivers, cars

app = FastAPI()

app.include_router(cars.router)
app.include_router(drivers.router)
