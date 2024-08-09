from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy import Column
from db.database import Base


class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    courses = relationship("DbCourse", back_populates='owner')


class DbCourse(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("DbUser", back_populates='courses')
