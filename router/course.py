from db import db_course
from db.database import get_db
from typing import List
from schemas import CourseBase, CourseDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(
    prefix='/course',
    tags=['course']
)


# Create course
@router.post('/', response_model=CourseDisplay)
def create_course(request: CourseBase, db: Session = Depends(get_db)):
    return db_course.create_course(db, request)


# Get course with id
@router.get('/{id}', response_model=Optional[CourseDisplay])
def get_course_by_id(id: int, db: Session = Depends(get_db)):
    return db_course.get_course(db, id)


# Delete course
@router.delete('/{id}')
def delete_course(id: int, db: Session = Depends(get_db)):
    return db_course.delete_course(db, id)

