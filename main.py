from fastapi import FastAPI, Depends, HTTPException, Query
# from sqlmodel import SQLModel, Field, Session, create_engine, select
from pydantic import BaseModel
from enum import Enum
# from typing import Annotated


# class Hero(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: int = Field(default=None, nullable=True)

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# sql_lite_file_name = "database.db"
# sqlite_url = f"sqlite:///{sql_lite_file_name}"
# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

# def get_session():
#     with Session(engine) as session:
#         yield session

# SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     create_db_and_tables()

# @app.post("/heroes/")
# async def create_hero(hero: Hero, session: SessionDep) -> Hero:
#     session.add(hero)
#     session.commit()
#     session.refresh(hero)
#     return hero

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    elif model_name == ModelName.resnet:
        return {"model_name": model_name, "message": "Have some residuals"}
    elif model_name == ModelName.lenet:
        return {"model_name": model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Unknown model"}

@app.get("/")
async def get_customers():
    return {"customers": ["Alice", "Bob", "Charlie"]}

@app.get("/customers/{customer_id}")
async def get_customer(customer_id: int):
    customers = ["Alice", "Bob", "Charlie"]
    if 0 <= customer_id < len(customers):
        return {"customer": customers[customer_id]}
    else:
        return {"error": "Customer not found"}, 404
    

@app.get("/getFullName/{first_name}/{last_name}")
async def get_full_name(first_name: str, last_name: str):
    full_name = f"{first_name} {last_name}"
    return {"full_name": full_name}