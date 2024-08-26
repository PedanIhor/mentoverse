from db import db_user
from db.database import get_db
from helpers.pagination import PagedResponseSchema, PageParams
from schemas import UserBase, UserDisplay, UserBaseForPatch
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user, CurrentUser
from helpers.exceptions_converter import exceptions_converter

router = APIRouter(
    prefix='/user',
    tags=['user']
)


# Create user
@router.post('/', response_model=UserDisplay, status_code=status.HTTP_201_CREATED)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Read all users
@router.get('/', response_model=PagedResponseSchema[UserDisplay])
def get_all_users(page_params: PageParams = Depends(), db: Session = Depends(get_db)):
    return db_user.get_all_users(db, page_params)


# Read user with id
@router.get('/{id}', response_model=UserDisplay)
@exceptions_converter
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return db_user.get_user_by_id(db, id)


# Update user
@router.put('/{id}', response_model=UserDisplay)
@exceptions_converter
def update_user(
        id: int,
        request: UserBase,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    if id is not current_user.id and not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        return db_user.update_user(db, id, request)


@router.patch('/{id}', response_model=UserDisplay)
@exceptions_converter
def update_user_by_patch(
        id: int,
        request: UserBaseForPatch,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    if id is not current_user.id and not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        db_user.update_by_patch(db, id, request)
        return db_user.get_user_by_id(db, id)


@router.post('/{user_id}/password', response_model=UserDisplay)
@exceptions_converter
def update_password(
        user_id: int,
        password: str,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    if user_id is not current_user.id and not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        return db_user.update_user_password(db, user_id, password)


# Delete user
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@exceptions_converter
def delete_user(id: int, db: Session = Depends(get_db), current_user: CurrentUser = Depends(get_current_user)):
    if id is not current_user.id and not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    else:
        db_user.delete_user(db, id)
