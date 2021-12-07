from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database
from typing import List
from sqlalchemy.orm import Session

router = APIRouter()

router = APIRouter(prefix="/api/blog", tags=["Blogs"])

# GET blogs
@router.get("/", response_model=List[schemas.ShowBlog])
def getBlogs(db: Session = Depends(database.get_db)):  # database instance
    blogs = db.query(models.Blog).all()

    return blogs


# GET /api/blog/id
@router.get("/{id}", response_model=schemas.ShowBlog)
def blogID(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog


# POST /api/blogs
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(blog_request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=blog_request.title, body=blog_request.body, user_id=blog_request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# DELETE /api/blog/id
@router.delete("/{id}")
def destroy(id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "deleted"


# UPDATE /api/blog/id
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id, request_blog: schemas.Blog, db: Session = Depends(database.get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    # or update by dict(request_blog) or request_blog.dict()
    blog.update(dict(request_blog))
    db.commit()
    return "Updated Blog"
