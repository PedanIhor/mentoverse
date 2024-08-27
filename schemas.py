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

    class Config:
        from_attributes = True


class CourseBase(BaseModel):
    title: str
    description: str


class CourseBaseForPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class CourseDisplay(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int

    class Config:
        from_attributes = True


class AppointmentBaseForPatch(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    starts: Optional[str] = None
    ends: Optional[str] = None
    tutor_id: Optional[int] = None
    students_ids: Optional[List[int]] = None


class AppointmentBase(BaseModel):
    title: str
    description: str
    starts: str
    ends: str
    tutor_id: int
    students_ids: List[int]


class AppointmentDisplay(BaseModel):
    id: int
    title: str
    description: str
    starts: str
    ends: str
    tutor_id: int

    class Config:
        from_attributes = True


class AppointmentParticipationBase(BaseModel):
    appointment_id: int
    student_id: int


class ReviewBase(BaseModel):
    course_id: int
    author_id: int
    title: str
    comment: str
    rating: int


class ReviewDisplay(BaseModel):
    id: int
    course_id: int
    author_id: int
    title: str
    comment: str
    rating: int

    class ConfigDict:
        from_attributes = True


class CommentDisplay(BaseModel):
    id: int
    title: str
    description: str
    user_id: int


class CommentBase(BaseModel):
    title: str
    description: str
    user_id: int
