from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database
from typing import List
from sqlalchemy.orm import Session
from ..hashing import Hash

router = APIRouter()

# refactor all tags into the router instead of adding it to each router path
router = APIRouter(prefix="/api/user", tags=["Users"])


# pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
###USER PATHS
# POST /api/users
def postUser(request_user: schemas.User, db: Session):
    # hashedPassword = pwd_cxt.hash(request_user.password)
    new_user = models.User(
        name=request_user.name, email=request_user.email, password=Hash.bcrypt(request_user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# GET /api/users
def getAllUsers(db: Session):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no users in DB")
    return users


# GET /api/users/:id
def getUserById(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    return user
