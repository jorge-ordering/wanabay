from typing import Generator, List
from app.models.user import User

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import cruds, models, schemas
from configs import security
# from app.core.config import settings
from configs.database import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/login"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.user.User:
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.token.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = cruds.user.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    if not crud.user.enabled(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return current_user

def get_current_permisions (
    roles: List[str] = [],
    current_user: models.user.User = Depends(get_current_user),
) -> str:
    if not "admin" in roles:
        pass
        raise HTTPException(
            status_code=401, detail="The user doesn't have enough privileges"
        )
    return current_user
