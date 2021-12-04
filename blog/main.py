from fastapi import FastAPI, Depends
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

# schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog")
def create(blog_request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog_request.title, body=blog_request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog")
def getBlogs(db: Session = Depends(get_db)):  # database instance
    blogs = db.query(models.Blog).all()
    return blogs
