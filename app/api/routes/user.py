from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import cruds, models, schemas
from app.schemas.user import User
from app.cruds import user

from app.api import deps
# from configs.security import settings
# from app.utils import send_new_account_email

router = APIRouter()

@router.get("/", response_model=List[schemas.user.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = cruds.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.user.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = cruds.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = cruds.user.create(db, obj_in=user_in)
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    return user


@router.put("/me", response_model=schemas.user.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.user.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = cruds.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.user.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=schemas.user.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    # if not settings.USERS_OPEN_REGISTRATION:
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Open user registration is forbidden on this server",
    #     )
    user = cruds.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = schemas.user.UserCreate(password=password, email=email, full_name=full_name)
    user = cruds.user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.user.User)
def read_user_by_id(
    user_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = cruds.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not cruds.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.user.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.user.UserUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = cruds.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = cruds.user.update(db, db_obj=user, obj_in=user_in)
    return user

@router.post("/firtsadmin", response_model=schemas.user.User)
def create_first(db: Session = Depends(deps.get_db)) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    # user = cruds.user.CRUDUser.get_by_username(db, username="superadmin")
    # if not user:
    user_in = schemas.user.UserCreate(
        username="superadmin",
        password="super",
        email="super@super.super",
        enabled=True
    )
    user = cruds.user.user.create(db, obj_in=user_in)
    return 'ok'
