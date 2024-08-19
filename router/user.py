from db import db_user
from db.database import get_db
from typing import List
from schemas import UserBase, UserDisplay, UserBaseForPatch
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from auth.oauth2 import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)


# Create user
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Read all users
@router.get('/', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)


# Read user with id
@router.get('/{id}', response_model=Optional[UserDisplay])
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db_user.get_user_by_id(db, id)
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# Update user
@router.put('/', response_model=UserDisplay)
def update_user(
        request: UserBase,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    user = db_user.get_user_by_username(db, current_user.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't find the user entity in the db")
    return db_user.update_user(db, user.id, request)


@router.patch('/', response_model=UserDisplay)
def update_user_by_patch(
        request: UserBaseForPatch,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    user = db_user.get_user_by_username(db, current_user.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't find the user entity in the db")
    db_user.update_by_patch(db, user.id, request)
    return db_user.get_user_by_id(db, user.id)


@router.post('/password', response_model=UserDisplay)
def update_password(
        password: str,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)):
    user = db_user.get_user_by_username(db, current_user.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404)
    return db_user.update_user_password(db, user.id, password)


# Delete user
@router.delete('/')
def delete_user(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    user = db_user.get_user_by_username(db, current_user.username)
    return db_user.delete_user(db, user.id)
