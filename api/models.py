from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Text, Integer
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

# Enum Definitions
class Status(enum.Enum):
    available = "Available"
    booked = "Booked"
    cancelled = "Cancelled"
    blocked = "Blocked"

class AppointmentStatus(enum.Enum):
    scheduled = "Scheduled"
    completed = "Completed"
    cancelled = "Cancelled"
    no_show = "NoShow"

# Availability Table
class Availability(Base):
    __tablename__ = "availability"
    id = Column(Integer, primary_key=True)
    provider_id = Column(String)  # Adjusted to String
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Enum(Status))

# Appointment Table
class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    patient_id = Column(String)  # Adjusted to String
    provider_id = Column(String)  # Adjusted to String
    scheduled_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Enum(AppointmentStatus))
    reason_for_visit = Column(Text)
    video_link = Column(String)