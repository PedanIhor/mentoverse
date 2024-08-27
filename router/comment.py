from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from schemas import CommentBase, CommentDisplay
from sqlalchemy.orm.session import Session
from db.database import get_db
from auth.oauth2 import CurrentUser, get_current_user
from db import db_comment
from helpers.exceptions_converter import exceptions_converter

router = APIRouter(
    prefix='/comment',
    tags=['comment']
)


# Create Comment
@router.post('/', response_model=CommentDisplay, status_code=status.HTTP_201_CREATED)
@exceptions_converter
def create_comment(request: CommentBase,
                   db: Session = Depends(get_db),
                   current_user: CurrentUser = Depends(get_current_user)):
    return db_comment.create_comment(request, db)


# Get Comment By ID
@router.get('/{id}', response_model=CommentDisplay)
@exceptions_converter
def get_comment_by_id(id: int,
                      db: Session = Depends(get_db),
                      current_user: CurrentUser = Depends(get_current_user)):
    comment = db_comment.get_comment_by_id(id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id {id} has no comments!')
    
    return comment


# Get Comment By UserID
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CommentDisplay])
@exceptions_converter
def get(user_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)):
    return db_comment.get_comment_by_user_id(db, user_id)


# Update A Comment
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=CommentDisplay)
@exceptions_converter
def update_comment(id: int, request: CommentBase,
                   db: Session = Depends(get_db),
                   current_user: CurrentUser = Depends(get_current_user)):
    return db_comment.update_comment(db, id, request)


# Delete A Comment
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@exceptions_converter
def delete_comment(id: int,
                   db: Session = Depends(get_db),
                   current_user: CurrentUser = Depends(get_current_user)):
    return db_comment.delete_comment(db, id)

    