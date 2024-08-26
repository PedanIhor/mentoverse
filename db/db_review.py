from sqlalchemy.orm import Session
from db.db_exceptions import DbException, DbExceptionReason
from db.models import DbReview, DbCourse
from schemas import ReviewBase


def get_reviews_by_course_id(course_id: int, db: Session):
    course = db.query(DbCourse).filter(DbCourse.id == course_id).first()
    return course.reviews


def create_review(db: Session, base: ReviewBase):
    review = DbReview(
        course_id=base.course_id,
        author_id=base.author_id,
        title=base.title,
        comment=base.comment,
        rating=base.rating
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def update_review(db: Session, review_id: int, base: ReviewBase):
    review_query = db.query(DbReview).filter(DbReview.id == review_id)
    entity = review_query.first()
    if not entity:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"Course with id: {id} not found!"
        )

    review_query.update({
        DbReview.title: base.title,
        DbReview.comment: base.comment,
        DbReview.rating: base.rating
    })
    db.commit()

    return entity


def delete_review(db: Session, review_id: int):
    review = db.query(DbReview).filter(DbReview.id == review_id).first()
    if not review:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"Course with id: {id} not found!"
        )
    db.delete(review)
    db.commit()
