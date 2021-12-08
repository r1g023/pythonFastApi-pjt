from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter()

router = APIRouter(prefix="/api/login", tags=["Authentication"])

# POST /api/login
@router.post("/", response_model=schemas.ShowUser)
def login(request: schemas.Login, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="invalid credentials")

    return user
