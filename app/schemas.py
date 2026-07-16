from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime
    class Config: from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None


class JobOut(BaseModel):
    id: int
    title: str
    company: str
    location: str
    type: str
    salary: str
    description: str
    created_at: datetime
    applicant_count: Optional[int] = 0
    class Config: from_attributes = True


class JobCreate(BaseModel):
    title: str
    company: str = "Gaint Clout"
    location: str = "Hyderabad"
    type: str = "Full-time"
    salary: str = ""
    description: str = ""


class ApplicationOut(BaseModel):
    id: int
    job_title: str
    company: str
    status: str
    ai_score: Optional[float] = None
    created_at: datetime
    class Config: from_attributes = True


class ApplicantOut(BaseModel):
    id: int
    name: str
    email: str
    applied_for: Optional[str] = None
    status: str
    ai_score: Optional[float] = None
    date: Optional[str] = None
    class Config: from_attributes = True


class StatusUpdate(BaseModel):
    status: str


class Token(BaseModel):
    access_token: str
    token_type: str