from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user, authentication


app = FastAPI()

# bind all models to engine
models.Base.metadata.create_all(bind=engine)

# ROUTERS
app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)
