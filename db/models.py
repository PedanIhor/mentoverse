from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.orm import (
    relationship,
    Mapped,
    validates,
    mapped_column,
    DeclarativeBase,
)
from sqlalchemy import Table, Column
from db.db_exceptions import DbException, DbExceptionReason


class Base(DeclarativeBase):
    pass


appointments_students_table=Table(
    'users_appointments',
    Base.metadata,
    Column("appointment_id", ForeignKey('appointments.id'), primary_key=True),
    Column("student_id", ForeignKey('users.id'), primary_key=True)
)


class DbUser(Base):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True, unique=True)
    admin = Column(Boolean)
    password = Column(String)
    courses = relationship("DbCourse", back_populates="owner")
    reviews = relationship('DbReview', back_populates='author')
    appointments = relationship(
        'DbAppointment',
        secondary=appointments_students_table,
        back_populates="students",
    )


class DbAppointment(Base):
    __tablename__ = 'appointments'
    id = mapped_column(Integer, primary_key=True, index=True)
    title = mapped_column(String)
    description = mapped_column(String)
    starts = mapped_column(String)
    ends = mapped_column(String)
    tutor_id = mapped_column(Integer, ForeignKey('users.id'), index=True)
    students = relationship(
        'DbUser',
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
    owner: Mapped["DbUser"] = relationship(back_populates='courses')
    reviews = relationship('DbReview', back_populates='course')


class DbReview(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    author_id = Column(Integer, ForeignKey('users.id'), index=True)
    author = relationship('DbUser', back_populates='reviews')
    course_id = Column(Integer, ForeignKey('courses.id'), index=True)
    course = relationship('DbCourse', back_populates='reviews')
    title = Column(String)
    comment = Column(String)

    @validates('rating')
    def validate_rating(self, _, value):
        if value < 1 or value > 5:
            raise DbException(DbExceptionReason.VALIDATION, detail="Rating must be from 1 to 5")
        return value
