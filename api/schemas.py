from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import enum

# Enum Definitions
class Status(str, enum.Enum):
    available = "Available"
    booked = "Booked"
    cancelled = "Cancelled"
    blocked = "Blocked"

class AppointmentStatus(str, enum.Enum):
    scheduled = "Scheduled"
    completed = "Completed"
    cancelled = "Cancelled"
    no_show = "NoShow"

# Availability Schema
class AvailabilityBase(BaseModel):
    provider_id: str
    start_time: datetime
    end_time: datetime
    status: Status

class AvailabilityCreate(AvailabilityBase):
    pass

class Availability(AvailabilityBase):
    id: int

# Appointment Schema
class AppointmentBase(BaseModel):
    patient_id: str
    provider_id: str
    start_time: datetime
    end_time: datetime
    reason_for_visit: str

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    video_link: str
    status: AppointmentStatus