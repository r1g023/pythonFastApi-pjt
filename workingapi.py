from fastapi import FastAPI

server = FastAPI()

inventory = {
    1: {
        "name": "Milk",
         "price": 3.99,
        "brand": "Regular"
    },
    2:   {
        "name": "mountain"
    }
}

@server.get("/")
def home(): 
    return {"Data": "testing"}

@server.get("/about")
def about(): 
    return {"Data": "about"}

@server.get("/get-item/{id}")
def get_item(id: int):
    return inventory[id]