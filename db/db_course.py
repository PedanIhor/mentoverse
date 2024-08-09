from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from db.models import DbCourse
from schemas import CourseBase


def create_course(db: Session, request: CourseBase):
    course = DbCourse(
        title=request.title,
        description=request.description,
        owner_id=request.owner_id
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return  course


def get_course(db: Session, id: int):
    course = db.query(DbCourse).filter(DbCourse.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with {id} not found!")
    return course


def delete_course(db: Session, id: int):
    course = db.query(DbCourse).filter(DbCourse.id == id).first()
    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Course with {id} not found!")
    db.delete(course)
    db.commit()
    return "OK"
