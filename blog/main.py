from fastapi import FastAPI, Depends, HTTPException, status, Response
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


# GET blogs
@app.get("/api/blogs")
def getBlogs(db: Session = Depends(get_db)):  # database instance
    blogs = db.query(models.Blog).all()
    if blogs:
        return blogs
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no users in DB")


# GET blog/id
@app.get("/api/blogs/{id}")
def blogID(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # HTTPException preferable but this is an alternate way
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail: " f"Blog wit the id {id} is not available"}
    return blog


# POST /api/blogs
@app.post("/api/blog", status_code=status.HTTP_201_CREATED)
def create(blog_request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blog_request.title, body=blog_request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# DELETE /api/blog/id
@app.delete("/api/blog/{id}")
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "deleted"


# UPDATE /api/blog/id
@app.put("/api/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id, request_blog: schemas.Blog, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    # or update by dict(request_blog) or request_blog.dict()
    blog.update(dict(request_blog))
    db.commit()
    return "Updated Blog"
