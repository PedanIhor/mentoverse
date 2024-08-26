from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user, CurrentUser
from db.database import get_db
from helpers.exceptions_converter import exceptions_converter
from db import db_review
from schemas import ReviewBase, ReviewDisplay
from typing import List


router = APIRouter(
    prefix='/review',
    tags=['review']
)


@router.get('', response_model=List[ReviewDisplay])
def get_reviews(course_id: int,
                db: Session = Depends(get_db)):
    return db_review.get_reviews_by_course_id(course_id, db)


@router.post('', response_model=ReviewDisplay, status_code=status.HTTP_201_CREATED)
@exceptions_converter
def review_course(request: ReviewBase,
                  db: Session = Depends(get_db),
                  current_user: CurrentUser = Depends(get_current_user)):
    if request.author_id is not current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db_review.create_review(db, request)


@router.put('/{id}', response_model=ReviewDisplay)
@exceptions_converter
def edit_review(id: int,
                request: ReviewBase,
                db: Session = Depends(get_db),
                current_user: CurrentUser = Depends(get_current_user)):
    if request.author_id is not current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db_review.update_review(db, id, request)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@exceptions_converter
def delete_review(id: int,
                  db: Session = Depends(get_db),
                  current_user: CurrentUser = Depends(get_current_user)):
    if id not in current_user.reviews_ids:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db_review.delete_review(db, id)
