from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

server = FastAPI()

# path = endpoint , GET = operation, server = path operation decorator
@server.get("/")
# path operation function
def index():
    return {"data": "blog list"}


@server.get("/blog")
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs from the db"}
    else:
        return {"data": f"{limit} blogs from the db"}


@server.get("/blog/{id}")
def show(id: int):
    return {"data": id}


@server.get("/blog/{id}/comments")
def comments(id: int):
    # fetch comments of blog with id = id
    return {"data": {"1", "2"}}


class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool]


@server.post("/blog")
def create_blog(blog: Blog):
    return {"data": f"blog is created with title as {blog.title}"}
