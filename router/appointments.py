from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from auth.oauth2 import get_current_user, CurrentUser
from schemas import AppointmentBase, AppointmentDisplay
from db import db_appointment, db_user
from typing import List
from helpers.db_action_wrapper import try_db_action

router = APIRouter(
    prefix='/appointments',
    tags=['appointments']
)


@router.get('/{id}', response_model=AppointmentDisplay)
def get_appointment_with_id(
        id: int,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    def action():
        return db_appointment.get_appointment_with_id(db, id)
    return try_db_action(action)


@router.get('/', response_model=List[AppointmentDisplay])
def get_user_appointments(
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user),
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
        current_user: CurrentUser = Depends(get_current_user)
):
    def action():
        if current_user.id is not request.tutor_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return db_appointment.create_appointment(db, request)
    return try_db_action(action)


# Delete the appointment
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(
        id: int,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    def action():
        user = db_user.get_user_by_username(db, current_user.username)
        appointment = db_appointment.get_appointment_with_id(db, id)
        if appointment.tutor_id is user.id:
            db_appointment.delete_appointment_with_id(db, id)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return appointment
    return try_db_action(action)
