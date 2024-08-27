from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from db.models import DbComment
from schemas import CommentBase
from typing import Optional
from db.db_exceptions import DbException, DbExceptionReason


# create comment
def create_comment(request: CommentBase, db: Session):
    new_comment = DbComment(
        title=request.title,
        description=request.description,
        user_id=request.user_id,
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return new_comment


# get comment by id
def get_comment_by_id(id: int, db: Session):
    comment = db.query(DbComment).filter(DbComment.id == id).first()
    if not comment:
        raise DbException(DbExceptionReason.NOT_FOUND, detail=f'user with id {id} has no comments!')
    return comment


# get comment by user id
def get_comment_by_user_id(db: Session, user_id: Optional[int] = None):
    commentQuery = db.query(DbComment)

    if user_id is not None:
        commentQuery = commentQuery.filter(DbComment.user_id == user_id)
    elif not user_id:
        raise DbException(DbExceptionReason.NOT_FOUND, detail=f"User id {user_id} not found!",
        )

    return commentQuery.all()


# update comment
def update_comment(db: Session, id: int, request: CommentBase):
    comment = db.query(DbComment).filter(DbComment.id == id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found!",
        )

    comment.update(
        {
            DbComment.title: request.title,
            DbComment.description: request.description,
            DbComment.user_id: request.user_id,
        }
    )
    db.commit()
    return comment.first()


# delete comment
def delete_comment(db: Session, id: int):
    comment = db.query(DbComment).filter(DbComment.id == id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found!",
        )
    db.delete(comment)
    db.commit()
