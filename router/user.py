from db import db_user
from db.database import get_db
from typing import List
from schemas import UserBase, UserDisplay, UserBaseForPatch
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user, CurrentUser
from helpers.db_action_wrapper import try_db_action

router = APIRouter(
    prefix='/user',
    tags=['user']
)


# Create user
@router.post('/', response_model=UserDisplay, status_code=status.HTTP_201_CREATED)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Read all users
@router.get('/', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)


# Read user with id
@router.get('/{id}', response_model=UserDisplay)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    def action():
        return db_user.get_user_by_id(db, id)
    return try_db_action(action)


# Update user
@router.put('/{id}', response_model=UserDisplay)
def update_user(
        id: int,
        request: UserBase,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    def action():
        if id is not current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        else:
            return db_user.update_user(db, id, request)
    return try_db_action(action)


@router.patch('/{id}', response_model=UserDisplay)
def update_user_by_patch(
        id: int,
        request: UserBaseForPatch,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    def action():
        if id is not current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        else:
            db_user.update_by_patch(db, id, request)
            return db_user.get_user_by_id(db, id)

    return try_db_action(action)


@router.post('/{user_id}/password', response_model=UserDisplay)
def update_password(
        user_id: int,
        password: str,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    def action():
        if user_id is not current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        else:
            return db_user.update_user_password(db, user_id, password)
    return try_db_action(action)


# Delete user
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    def action():
        if id is not current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        else:
            db_user.delete_user(db, current_user.id)
    try_db_action(action)
