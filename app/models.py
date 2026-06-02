from datetime import datetime
from enum import Enum

from pydantic import field_validator
from sqlmodel import Field, SQLModel

# I am using the enum class to define the possible values for the sport, status, and winner fields.
# I am using the str and not Enum class becasue of two reasons:
# 1. DB storage — SQLite stores them as strings ("scheduled"), not opaque enum objects.
# 2. JSON serialisation — FastAPI serialises them as strings ("scheduled") instead of {"name": "SCHEDULED", "value": "scheduled"}.

class Sport(str, Enum):
    FOOTBALL = "football"
    BASKETBALL = "basketball"
    TENNIS = "tennis"
    OTHER = "other"

class Status(str, Enum):
    SCHEDULED = "scheduled"
    LIVE = "live"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Winner(str, Enum):
    HOME = "home"
    AWAY = "away"
    DRAW = "draw"


class EventBase(SQLModel):
    name: str
    sport: Sport
    start_time: datetime
    status: Status
    venue: str | None = None

    @field_validator('start_time')
    @classmethod
    def validate_start_time(cls, v):
        if v.tzinfo is None:
            raise ValueError("start_time must include a timezone offset (e.g. '2026-06-03T14:00:00+01:00' or '...Z')")
        return v

class Event(EventBase,table=True):
    id: int | None = Field(default=None, primary_key=True)
    status: Status = Field(default=Status.SCHEDULED)

class EventCreate(EventBase):
    # No additional fields for creation
    pass

# Read model includes the id and status fields
class EventRead(EventBase):
    id: int
    status: Status


class ResultBase(SQLModel):
    winner: Winner
    home_score: int | None = None
    away_score: int | None = None

class Result(ResultBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="event.id", unique=True, index=True)


class ResultCreate(ResultBase):
    # No additional fields for creation
    pass

class ResultRead(ResultBase):
    id: int
    event_id: int
