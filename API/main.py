from fastapi import FastAPI
from routers import cars, drivers

app = FastAPI()

app.include_router(cars.router)
app.include_router(drivers.router)

