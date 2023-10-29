from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
from project.database import database, User, Movie, UserReview
from project.routers import router as api_router
import os

app = FastAPI(
    title="fastAPI Demo",
    version="1.0.0",
)

app.include_router(api_router)


@app.on_event("startup")
def startup():
    print("startup")
    if database.is_closed():
        database.connect()
        print("database connected")
    database.create_tables([User, Movie, UserReview])


@app.on_event("shutdown")
def shutdown():
    print("shutdown")
    if not database.is_closed():
        database.close()
        print("database closed")


@app.get("/")
def read_root():
    return {"Hello": "World"}
