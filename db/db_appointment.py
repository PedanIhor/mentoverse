from sqlalchemy.orm import Session
from schemas import AppointmentBase, UserBase
from db.models import DbAppointment, DbUser
from typing import List


# Create an appointment
def create_appointment(db: Session, request: AppointmentBase):
    students = db.query(DbUser).filter(
        DbUser.id.in_(request.students_ids)
    ).all()
    appointment = DbAppointment(
        title=request.title,
        description=request.description,
        starts=request.starts,
        ends=request.ends,
        tutor_id=request.tutor_id,
        students=students
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


# Get all user's appointments
def get_users_appointments(db: Session, user_id: int):
    as_tutor = db.query(DbAppointment).filter(
        DbAppointment.tutor_id == user_id
    ).all()
    as_student = db.query(DbAppointment).filter(
        DbAppointment.students.any(id=user_id)
    ).all()
    return as_tutor + as_student

    # return db.query(DbAppointment).filter(
    #     DbAppointment.tutor_id == user_id or DbAppointment.students.any(id=user_id)
    # ).all()
