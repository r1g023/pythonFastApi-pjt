from pydantic import BaseModel
from typing import List

# pydantic models
# BLOG
class BlogBase(BaseModel):
    title: str
    body: str
    user_id: int


class Blog(BlogBase):
    class Config:
        orm_mode = True


# USER CLASS
class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    password: str
    blogs: List[Blog] = []

    class Config:
        orm_mode = True


# BLOG
# extend Blog class into ShowBlog
class ShowBlog(BaseModel):
    id: int
    title: str
    body: str
    creator: ShowUser

    class Config:
        orm_mode = True
