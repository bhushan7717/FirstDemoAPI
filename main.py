from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

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