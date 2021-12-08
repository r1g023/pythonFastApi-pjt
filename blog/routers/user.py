from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, database
from typing import List
from sqlalchemy.orm import Session
from ..hashing import Hash
from ..repository import user

router = APIRouter()

# refactor all tags into the router instead of adding it to each router path
router = APIRouter(prefix="/api/user", tags=["Users"])


# pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
###USER PATHS
# POST /api/users
@router.post("/", response_model=schemas.ShowUser)  # pydantic model
def create_user(request_user: schemas.User, db: Session = Depends(database.get_db)):
    return user.postUser(request_user, db)


# GET /api/users
@router.get("/", response_model=List[schemas.ShowUser])
def getUsers(db: Session = Depends(database.get_db)):
    return user.getAllUsers(db)


# GET /api/users/:id
@router.get("/{id}", response_model=schemas.ShowUser)
def getUserId(id: int, db: Session = Depends(database.get_db)):
    return user.getUserById(id, db)
