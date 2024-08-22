from sqlalchemy.orm import Session
from sqlalchemy import or_
from schemas import AppointmentBase, AppointmentBaseForPatch
from db.models import DbAppointment, DbUser
from db.db_exceptions import DbException, DbExceptionReason


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
    return db.query(DbAppointment).where(
        or_(
            DbAppointment.tutor_id == user_id,
            DbAppointment.students.any(id=user_id))
    ).all()
    # return db.query(DbAppointment).filter(
    #     DbAppointment.tutor_id == user_id or DbAppointment.students.any(id=user_id)
    # ).all()


# Get appointment with id
def get_appointment_with_id(db: Session, id: int):
    appointment = db.query(DbAppointment).filter(DbAppointment.id == id).first()
    if not appointment:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"Appointment with id: {id} not found!"
        )
    return appointment


# Delete an appointment with id
def delete_appointment_with_id(db: Session, id: int):
    appointment = db.query(DbAppointment).filter(DbAppointment.id == id)
    if not appointment:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"Appointment with id: {id} not found!"
        )
    db.delete(appointment)
    db.commit()


# Update an appointment with provided dictionary
def update_appointment_with_dict(
        db: Session,
        id: int,
        updates: dict
):
    appointment = db.query(DbAppointment).filter(DbAppointment.id == id)
    if not appointment:
        raise DbException(
            DbExceptionReason.NOT_FOUND,
            detail=f"Appointment with id: {id} not found!"
        )
    appointment.update(updates)
    db.commit()
    return appointment.first()


# Update an appointment with AppointmentBaseForPatch
def update_appointment_with_request(
        db: Session,
        id: int,
        request: AppointmentBaseForPatch
):

    return update_appointment_with_dict(db, id, _map_patch_model(db, id, request))


def _map_patch_model(db: Session, id: int, request: AppointmentBaseForPatch):
    updates = {}

    if request.title is not None:
        updates[DbAppointment.title] = request.title

    if request.description is not None:
        updates[DbAppointment.description] = request.description

    if request.starts is not None:
        updates[DbAppointment.starts] = request.starts

    if request.ends is not None:
        updates[DbAppointment.ends] = request.ends

    if request.tutor_id is not None:
        updates[DbAppointment.tutor_id] = request.tutor_id

    if request.students_ids is not None:
        students = db.query(DbUser).filter(
            DbUser.appointments.any(id=id) and DbUser.id.in_(request.students_ids)
        ).all()
        updates[DbAppointment.students] = students

    return updates

