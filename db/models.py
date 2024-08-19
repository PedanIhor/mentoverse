from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy.orm import (
    relationship,
    Mapped,
    validates,
    mapped_column,
    DeclarativeBase,
)
from sqlalchemy import Table, Column, TIMESTAMP
from db.db_exceptions import DbException
from typing import List


class Base(DeclarativeBase):
    pass



class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True, unique=True)
    password = Column(String)
    courses = relationship("DbCourse", back_populates='owner')


class DbCourse(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("DbUser", back_populates='courses')
