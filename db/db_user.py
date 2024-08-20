from sqlalchemy.orm.session import Session
from db.hash import Hash
from db.models import DbUser
from schemas import UserBase, UserBaseForPatch
from db.db_exceptions import DbException, DbExceptionReason


def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_all_users(db: Session):
    return db.query(DbUser).all()


def get_user_by_id(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"User with id: {id} not found!"
        )
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(DbUser).filter(DbUser.username == username).first()
    if not user:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"User with username: {username} not found!"
        )
    return user


def update_user_with_changes(db: Session, id: int, changes: dict):
    user = db.query(DbUser).filter(DbUser.id == id)
    if not user:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"User with id: {id} not found!"
        )
    user.update(changes)
    db.commit()
    return user.first()


def update_user(db: Session, id: int, request: UserBase):
    return update_user_with_changes(db, id, {
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password),
    })


def update_by_patch(db: Session, id: int, request: UserBaseForPatch):
    return update_user_with_changes(db, id, map_patch_model(request))


def update_user_password(db: Session, id: int, password: str):
    return update_user_with_changes(db, id, {
        DbUser.password: Hash.bcrypt(password)
    })


def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    if not user:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"User with id: {id} not found!"
        )
    db.delete(user)
    db.commit()


def map_patch_model(model: UserBaseForPatch):
    updates = {}

    if model.username is not None:
        updates[DbUser.username] = model.username

    if model.email is not None:
        updates[DbUser.email] = model.email

    return updates
