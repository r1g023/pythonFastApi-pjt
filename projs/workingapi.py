from fastapi import FastAPI, Path, Query, HTTPException
from typing import Optional
from pydantic import BaseModel

server = FastAPI()

inventory = {
    1: {"name": "Milk", "price": 3.99, "brand": "Regular"},
    2: {"name": "mountain", "price": 1.99, "brand": "yo"},
    3: {"name": "mountain", "price": 2.50, "brand": "flo"},
}


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


@server.get("/")
def home():
    if inventory:
        return inventory


@server.get("/about")
def about():
    return {"Data": "about"}


@server.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item youd like", gt=0)):
    return inventory[item_id]


@server.get("/get-by-name/{item_id}")
def get_item(*, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    raise HTTPException(status_code=405, detail="item")


@server.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=404, detail="ID already exists in the database")

    inventory[item_id] = item
    return inventory[item_id]


@server.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="ID DOES NOT exist in the database")

    inventory[item_id] = item

    return inventory[item_id]


@server.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The id of item to delete", ge=0)):
    if item_id not in inventory:
        return {"Error": "id does not exist"}

    del inventory[item_id]
    return {"Success": "item deleted!"}
