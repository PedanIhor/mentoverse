from db import db_course, db_user
from db.database import get_db
from typing import List
from schemas import CourseBase, CourseDisplay, UserBase, UserDisplay, Course
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from auth.oauth2 import get_current_user
from exceptions import MentoverseException

router = APIRouter(
    prefix='/course',
    tags=['course']
)


# Create course
@router.post('/', response_model=CourseDisplay)
def create_course(
        request: CourseBase,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    if "mentoverse" in request.title or "mentoverse" in request.description:
        raise MentoverseException("Don't use mentoverse platform name in your course!")
    user = db_user.get_user_by_username(db, current_user.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Couldn't find a user for the token")
    return db_course.create_course(db, request, user.id)


# Edit course
@router.put('/{id}', response_model=CourseDisplay)
def put_course(
        id: int,
        request: CourseBase,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    user = db_user.get_user_by_username(db, current_user.username)
    if not _is_user_owner_of_course_id(id, user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db_course.update_course_by_request(db, id, request)
    return db_course.get_course(db, id)


@router.patch('/{id}', response_model=CourseDisplay)
def patch_course(
        id: int,
        request: CourseBase,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    user = db_user.get_user_by_username(db, current_user.username)
    if not _is_user_owner_of_course_id(id, user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    updates = request.model_dump(exclude_unset=True)
    db_course.update_course_by_dict(db, id, updates)
    return db_course.get_course(db, id)


# Get course with id
@router.get('/{id}', response_model=Optional[CourseDisplay])
def get_course_by_id(id: int, db: Session = Depends(get_db)):
    return db_course.get_course(db, id)


# Delete course
@router.delete('/{id}')
def delete_course(
        id: int,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    user = db_user.get_user_by_username(db, current_user.username)
    if not _is_user_owner_of_course_id(id, user):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db_course.delete_course(db, id)
    return {'message': 'OK'}


# Get all courses
@router.get("/", response_model=List[CourseDisplay])
def get_all_courses(db: Session = Depends(get_db)):
    return db_course.get_all_courses(db)


# Get all courses by owner id
@router.get('/owner-id/{owner_id}', response_model=List[CourseDisplay])
def get_courses_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    return db_course.get_courses_by_owner_id(db, owner_id)


def _map_user_courses_to_ids(course: Course):
    return course.id


def _is_user_owner_of_course_id(course_id: int, user: UserDisplay):
    courses_ids = map(_map_user_courses_to_ids, user.courses)
    return course_id in courses_ids
