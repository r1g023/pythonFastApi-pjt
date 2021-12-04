from fastapi import FastAPI, Depends, HTTPException, status
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

# schemas

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency Middleware
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# raise HTTPException(status_code=404, detail="ID already exists in the database")

# POST /api/blogs
@app.post("/api/blog", status_code=status.HTTP_201_CREATED)
def create(blog_request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog_request.title, body=blog_request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# GET blogs
@app.get("/api/blogs")
def getBlogs(db: Session = Depends(get_db)):  # database instance
    blogs = db.query(models.Blog).all()
    if blogs:
        return blogs
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no users in DB")


# GET blog/id
@app.get("/api/blogs/{id}")
def blogID(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog
