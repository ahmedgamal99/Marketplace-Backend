from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from src.database import get_db
from src.models.user import User
from src.schemas.user import TokenData
from dotenv import load_dotenv
import os


class Authentication:
    load_dotenv()
    SECRET_KEY = os.environ["SECRET_KEY"]
    ALGORITHM = os.environ["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["EXPIRE_MINUTES"]
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    scheme = HTTPBearer()

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_hashed_password(self, plain_password):
        return self.pwd_context.hash(plain_password)

    def get_user(self, email: str, db: Session = Depends(get_db)):
        user = db.query(User).filter(User.email == email).first()

        return user

    def authenticate_user(self,  email: str, password: str, db: Session = Depends(get_db)):
        user = self.get_user(email, db=db)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    def create_access_token(self, data: dict):

        to_encode = data.copy()

        # expire = datetime.utcnow() + self.ACCESS_TOKEN_EXPIRE_MINUTES
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.SECRET_KEY,
                                 algorithms=[self.ALGORITHM])
            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail='Signature has expired')

        except Exception as E:
            raise HTTPException(
                status_code=401, detail='Invalid token')

        # except jwt.InvalidTokenError as invalid:
            # raise HTTPException(status_code=401, detail='Invalid token')

        # except jwt.InvalidTokenError as invalid:
        #     raise HTTPException(status_code=401, detail='Invalid token')

    async def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(scheme)):
        return self.decode_token(auth.credentials)

    async def get_current_active_user(current_user: User = Depends(get_current_user)):
        return current_user
