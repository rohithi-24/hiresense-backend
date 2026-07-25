from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="applicant")  # "applicant" | "admin"
    profile_views = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    applications = relationship("Application", back_populates="user")


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, default="Gaint Clout")
    location = Column(String, default="Hyderabad")
    type = Column(String, default="Full-time")  # Full-time | Internship | Contract
    salary = Column(String, default="")
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    applications = relationship("Application", back_populates="job")


class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    cover_letter = Column(Text, default="")
    skills = Column(String, default="")
    resume_path = Column(String, default="")
    ai_score = Column(Float, default=0)
    status = Column(String, default="under_review")
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")


class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)