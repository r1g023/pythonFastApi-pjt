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
@router.post("/", response_model=schemas.ShowUser)  # pydantic model
def create_user(request_user: schemas.User, db: Session = Depends(database.get_db)):
    # hashedPassword = pwd_cxt.hash(request_user.password)
    new_user = models.User(
        name=request_user.name, email=request_user.email, password=Hash.bcrypt(request_user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# GET /api/users
@router.get("/", response_model=List[schemas.ShowUser])
def getUsers(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no users in DB")
    return users


# GET /api/users/:id
@router.get("/{id}", response_model=schemas.ShowUser)
def getUserId(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no users in DB")
    return user
