from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas

# GET /api/blogs
def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no users in db")
    return blogs


# GET /api/blogs/:Id
def getById(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    return blog


# POST /api/blogs
def create(blog_request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=blog_request.title, body=blog_request.body, user_id=blog_request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


# DELETE /api/blogs/:id
def deleteBlog(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return "deleted"


# UPDATE /api/blogs/:id
def updateBlog(id: int, request_blog: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    # or update by dict(request_blog) or request_blog.dict()
    blog.update(dict(request_blog))
    db.commit()
    return "Updated Blog"
