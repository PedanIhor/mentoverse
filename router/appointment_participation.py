from fastapi import APIRouter, Depends, HTTPException, status
from auth.oauth2 import get_current_user, CurrentUser
from db.database import get_db
from sqlalchemy.orm import Session
from db import db_appointment
from schemas import AppointmentParticipationBase
from helpers.exceptions_converter import exceptions_converter

router = APIRouter(
    prefix='/appointmentParticipation',
    tags=['appointments']
)


# Adds student to the appointment
@router.post('/', status_code=status.HTTP_201_CREATED)
@exceptions_converter
def create_appointment_participation(
        request: AppointmentParticipationBase,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user)
):
    if current_user.id is not request.student_id and not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db_appointment.assign_student_for_appointment(
        db, request.appointment_id, request.student_id
    )


# Removes student's participation from appointment
@router.delete('/{appointment_id}/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
@exceptions_converter
def delete_student_participation(
        appointment_id: int,
        student_id: int,
        db: Session = Depends(get_db),
        current_user: CurrentUser = Depends(get_current_user),
):
    if current_user.id is not student_id and not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    db_appointment.unassign_student_for_appointment(
        db, appointment_id, student_id
    )
