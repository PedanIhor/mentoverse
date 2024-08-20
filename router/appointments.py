from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from auth.oauth2 import get_current_user
from schemas import AppointmentBase, AppointmentDisplay, UserBase
from db import db_appointment, db_user
from typing import List
from helpers.db_action_wrapper import try_db_action

router = APIRouter(
    prefix='/appointments',
    tags=['appointments']
)


@router.get('/', response_model=List[AppointmentDisplay])
def get_user_appointments(
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user),
):
    def action():
    user = db_user.get_user_by_username(db, current_user.username)
    return db_appointment.get_users_appointments(db, user.id)
    return try_db_action(action)


# Create an appointment
@router.post('/', response_model=AppointmentDisplay, status_code=status.HTTP_201_CREATED)
def create_appointment(
        request: AppointmentBase,
        db: Session = Depends(get_db),
        current_user: UserBase = Depends(get_current_user)
):
    return db_appointment.create_appointment(db, request)
