from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database
from typing import List
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter()

router = APIRouter(prefix="/api/blog", tags=["Blogs"])

# GET blogs
@router.get("/", response_model=List[schemas.ShowBlog])
def getBlogs(db: Session = Depends(database.get_db)):  # database instance
    return blog.get_all(db)  # GET FROM REPOSITORY folder


# GET /api/blog/id
@router.get("/{id}", response_model=schemas.ShowBlog)
def blogID(id: int, db: Session = Depends(database.get_db)):
    return blog.getById(id, db)


# POST /api/blogs -
@router.post("/", status_code=status.HTTP_201_CREATED)
def create(blog_request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create(blog_request, db)  # GET FROM REPOSITORY folder


# DELETE /api/blog/id
@router.delete("/{id}")
def destroy(id: int, db: Session = Depends(database.get_db)):
    return blog.deleteBlog(id, db)


# UPDATE /api/blog/id
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def updateBlog(id: int, request_blog: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.updateBlog(id, request_blog, db)
