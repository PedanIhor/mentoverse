from typing import Optional, List
from pydantic import BaseModel


# Course inside UserDisplay
class Course(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: str
    password: str


class UserBaseForPatch(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


class UserDisplay(BaseModel):
    id: int
    username: str
    email: str
    courses: List[Course] = []

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    title: str | None
    description: str | None


class CourseDisplay(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int

    class Config:
        from_attributes = True
