from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.orm import (
    relationship,
    Mapped,
    validates,
    mapped_column,
    DeclarativeBase,
)
from sqlalchemy import Table, Column, TIMESTAMP
from db.db_exceptions import DbException, DbExceptionReason
from typing import List


class Base(DeclarativeBase):
    pass


appointments_students_table = Table(
    'users_appointments',
    Base.metadata,
    Column("appointment_id", ForeignKey('appointments.id'), primary_key=True),
    Column("student_id", ForeignKey('users.id'), primary_key=True)
)


class DbUser(Base):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True, index=True)
    username = mapped_column(String, index=True, unique=True)
    email = mapped_column(String, index=True, unique=True)
    password = mapped_column(String)
    courses = relationship("DbCourse", back_populates="owner")
    appointments: Mapped[List['DbAppointment']] = relationship(
        secondary=appointments_students_table,
        back_populates="students"
    )


class DbAppointment(Base):
    __tablename__ = 'appointments'
    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String)
    description = mapped_column(String)
    starts = mapped_column(TIMESTAMP)
    ends = mapped_column(TIMESTAMP)
    tutor_id = mapped_column(Integer, ForeignKey('users.id'), index=True)
    students: Mapped[List['DbUser']] = relationship(
        secondary=appointments_students_table,
        back_populates="appointments"
    )

    @validates('title')
    def validate_title(self, _, value):
        if len(value) > 60:
            raise DbException(DbExceptionReason.VALIDATION, detail="title must be less or equal 60 symbols")
        return value

    @validates('description')
    def validate_description(self, _, value):
        if len(value) > 180:
            raise DbException(DbExceptionReason.VALIDATION, detail="description must be less or equal 180 symbols")
        return value


class DbCourse(Base):
    __tablename__ = 'courses'
    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String)
    description = mapped_column(String)
    owner_id = mapped_column(Integer, ForeignKey('users.id'), index=True)
    owner: Mapped["DbUser"] = relationship(back_populates="courses")
