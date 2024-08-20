from db import db_user
from db.database import get_db
from typing import List
from schemas import UserBase, UserDisplay, UserBaseForPatch
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional
from auth.oauth2 import get_current_user
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
@router.put('/', response_model=UserDisplay)
def update_user(
        request: UserBase,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    def action():
        user = db_user.get_user_by_username(db, current_user.username)
        return db_user.update_user(db, user.id, request)
    return try_db_action(action)


@router.patch('/', response_model=UserDisplay)
def update_user_by_patch(
        request: UserBaseForPatch,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    def action():
        user = db_user.get_user_by_username(db, current_user.username)
        db_user.update_by_patch(db, user.id, request)
        return db_user.get_user_by_id(db, user.id)

    return try_db_action(action)


@router.post('/password', response_model=UserDisplay)
def update_password(
        password: str,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)):
    def action():
        user = db_user.get_user_by_username(db, current_user.username)
        return db_user.update_user_password(db, user.id, password)
    return try_db_action(action)


# Delete user
@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    def action():
        user = db_user.get_user_by_username(db, current_user.username)
        db_user.delete_user(db, user.id)
    try_db_action(action)
