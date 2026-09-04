from enum import Enum


class GoalType(str, Enum):
    TIME = "time"
    CONTENT = "content"
    QUESTIONS = "questions"


class GoalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
