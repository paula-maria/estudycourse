from datetime import date
from pydantic import BaseModel


class ProgressResponse(BaseModel):
    total_sessions: int
    completed_sessions: int
    pending_sessions: int
    total_minutes: int
    total_hours: float
    progress_percentage: float


class SubjectProgressResponse(BaseModel):
    subject_id: int
    subject_name: str
    total_sessions: int
    completed_sessions: int
    pending_sessions: int
    total_minutes: int
    total_hours: float
    progress_percentage: float


class DailyProgressResponse(BaseModel):
    date: date
    minutes_studied: int
    sessions_completed: int


class DashboardResponse(BaseModel):
    summary: ProgressResponse
    subjects: list[SubjectProgressResponse]
    daily_progress: list[DailyProgressResponse]