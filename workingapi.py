from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

server = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


inventory = {
    1: {"name": "Milk", "price": 3.99, "brand": "Regular"},
    2: {"name": "mountain", "price": 1.99, "brand": "yo"},
    3: {"name": "mountain", "price": 2.50, "brand": "flo"},
}


@server.get("/")
def home():
    return inventory


@server.get("/about")
def about():
    return {"Data": "about"}


@server.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item youd like", gt=0)):
    return inventory[item_id]


@server.get("/get-by-name/{item_id}")
def get_item(*, item_id: int, name: Optional[str] = None, test: int):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not found"}


@server.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        return {"error": "Item ID already exists"}

    inventory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
    return inventory[item_id]
