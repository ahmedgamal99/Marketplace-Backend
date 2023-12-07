from fastapi import APIRouter, Depends, HTTPException, status
from src.utils.auth import Authentication
from src.schemas.user import CreateUser, LoginUser
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User

auth_router = APIRouter()
auth = Authentication()


@auth_router.post('/signup')
async def signup(details: CreateUser, db: Session = Depends(get_db)):

    fetch_user = db.query(User).filter_by(email=details.email).all()

    if fetch_user:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Email already exists!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    hashed_password = auth.get_hashed_password(
        plain_password=details.password1)

    to_create = User(
        name=details.name,
        email=details.email,
        password=hashed_password,
    )

    db.add(to_create)
    db.commit()
    return {
        "success": True,
        "created_id": to_create.user_id
    }


@auth_router.post("/login")
async def login(details: LoginUser, db: Session = Depends(get_db)):
    user = auth.authenticate_user(details.email, details.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    data = {
        "id": user.user_id,
        "email": user.email
    }
    token = auth.create_access_token(data)
    return {
        "user_id": user.user_id,
        "email": user.email,
        "token": token
    }

    # get_user(self, email: str, db: Session = Depends(get_db)):
    # def verify_password(self, plain_password, hashed_password):


# @auth_router.get("/protected")
# async def protected(user: str = Depends(auth.get_current_user), db: Session = Depends(get_db)):
#     return user
