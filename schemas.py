from typing import Optional, List
from pydantic import BaseModel


# Course inside UserDisplay
class Course(BaseModel):
    title: str
    description: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserBaseForPatch(BaseModel):
    username: Optional[str]
    email: Optional[str]


class UserDisplay(BaseModel):
    username: str
    email: str
    courses: List[Course] = []

    class Config:
        from_attributes = True


# User inside ArticleDisplay
class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    title: str
    description: str
    creator_id: int


class CourseDisplay(BaseModel):
    id: int
    title: str
    description: str
    owner: User

    class Config:
        from_attributes = True
