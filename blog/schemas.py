from pydantic import BaseModel

# pydantic model
class Blog(BaseModel):
    title: str
    body: str


# extend Blog class into ShowBlog
class ShowBlog(BaseModel):
    id: int
    title: str
    body: str

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

    class Config:
        orm_mode = True
