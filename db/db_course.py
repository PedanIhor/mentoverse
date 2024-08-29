from sqlalchemy.orm.session import Session
from sqlalchemy.orm.query import Query
from db.models import DbCourse
from helpers.pagination import PageParams, PagedResponseSchema, paginate
from schemas import CourseBase, CourseDisplay
from db.db_exceptions import DbException, DbExceptionReason


def create_course(db: Session, request: CourseBase, owner_id: int):
    course = DbCourse(
        title=request.title,
        description=request.description,
        owner_id=owner_id
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get_all_courses(db: Session, page_params: PageParams):
    return paginate(page_params, db.query(DbCourse))


def get_courses_by_owner_id_paginated(db: Session, owner_id: int, page_params: PageParams):
    return paginate(page_params, db.query(DbCourse).filter(DbCourse.owner_id == owner_id))


def get_courses_by_owner_id(db: Session, owner_id: int):
    return db.query(DbCourse).filter(DbCourse.owner_id == owner_id)


def get_course(db: Session, id: int):
    course = db.query(DbCourse).filter(DbCourse.id == id).first()
    if not course:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"Course with id: {id} not found!"
        )
    return course


def delete_course(db: Session, id: int):
    course = db.query(DbCourse).filter(DbCourse.id == id).first()
    if not course:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"Course with id: {id} not found!"
        )
    db.delete(course)
    db.commit()


def update_course_with_changes(db: Session, course: Query, updates: dict[str, any]):
    course.update(updates)
    db.commit()


def update_course_by_dict(db: Session, id: int, updates: dict[str, any]):
    course_query = db.query(DbCourse).filter(DbCourse.id == id)
    entity = course_query.first()
    if not entity:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"Course with id: {id} not found!"
        )
    update_course_with_changes(db, course_query, updates)
    return entity


def update_course_by_request(db: Session, id: int, request: CourseBase):
    course_query = db.query(DbCourse).filter(DbCourse.id == id)
    if not course_query.first():
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"Course with id: {id} not found!"
        )
    update_course_with_changes(db, course_query, {
        DbCourse.title: request.title,
        DbCourse.description: request.description
    })
    return course_query.first()
