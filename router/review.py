from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user, CurrentUser
from db.database import get_db

router = APIRouter(
    prefix='/review',
    tags=['review']
)


@router.post('/')
def review_course(course_id: int,
                  db: Session = Depends(get_db),
                  current_user: CurrentUser = Depends(get_current_user)):
    return "ok"
