from db import db_course
from db.database import get_db
from typing import List
from helpers.pagination import PagedResponseSchema, PageParams
from schemas import CourseBase, CourseDisplay, CourseBaseForPatch
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user, CurrentUser
from helpers.exceptions_converter import exceptions_converter

router = APIRouter(
    prefix='/course',
    tags=['course']
)


# Create course
@router.post(
    '/',
    response_model=CourseDisplay,
    status_code=status.HTTP_201_CREATED
)
@exceptions_converter
def create_course(
        request: CourseBase,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    return db_course.create_course(db, request, current_user.id)


# Edit course
@router.put('/{id}', response_model=CourseDisplay)
@exceptions_converter
def put_course(
        id: int,
        request: CourseBase,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    if not _is_user_owner_of_course_id(db, id, current_user.id) and not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db_course.update_course_by_request(db, id, request)


@router.patch('/{id}', response_model=CourseDisplay)
@exceptions_converter
def patch_course(
        id: int,
        request: CourseBaseForPatch,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    if not _is_user_owner_of_course_id(db, id, current_user.id) and not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    updates = request.model_dump(exclude_none=True)
    db_course.update_course_by_dict(db, id, updates)
    return db_course.get_course(db, id)


# Get course with id
@router.get('/{id}', response_model=CourseDisplay)
@exceptions_converter
def get_course_by_id(id: int, db: Session = Depends(get_db)):
    return db_course.get_course(db, id)


# Delete course
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
@exceptions_converter
def delete_course(
        id: int,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    if not _is_user_owner_of_course_id(db, id, current_user.id) and not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db_course.delete_course(db, id)


# Get all courses
@router.get("/", response_model=PagedResponseSchema[CourseDisplay])
def get_all_courses(page_params: PageParams = Depends(), db: Session = Depends(get_db)):
    return db_course.get_all_courses(db, page_params)


# Get all courses by owner id
@router.get('/owner-id/{owner_id}', response_model=List[CourseDisplay])
def get_courses_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    return db_course.get_courses_by_owner_id(db, owner_id)


def _is_user_owner_of_course_id(db: Session, course_id: int, user_id: int):
    db_courses = db_course.get_courses_by_owner_id(db, user_id)
    filtered = list(filter(lambda x: x if x.id == course_id else None, db_courses))
    return len(filtered) > 0
