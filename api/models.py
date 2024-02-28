
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from .database import Base
import enum

class Role(enum.Enum):
    patient = "Patient"
    healthcare_provider = "Healthcare Provider"
    administrator = "Administrator"

class Status(enum.Enum):
    available = "Available"
    booked = "Booked"
    cancelled = "Cancelled"
    blocked = "Blocked"

class NotificationType(enum.Enum):
    appointment_reminder = "AppointmentReminder"
    appointment_change = "AppointmentChange"

class AppointmentStatus(enum.Enum):
    scheduled = "Scheduled"
    completed = "Completed"
    cancelled = "Cancelled"
    no_show = "NoShow"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(Enum(Role))
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)

class HealthcareProvider(Base):
    __tablename__ = "healthcare_providers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    specialization = Column(String)
    bio = Column(Text)
    license_number = Column(String)
    user = relationship("User")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date_of_birth = Column(DateTime)
    gender = Column(String)
    medical_history_summary = Column(Text)
    user = relationship("User")

class Availability(Base):
    __tablename__ = "availability"
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey('healthcare_providers.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Enum(Status))

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    provider_id = Column(Integer, ForeignKey('healthcare_providers.id'))
    scheduled_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Enum(AppointmentStatus))
    reason_for_visit = Column(Text)

class AppointmentFeedback(Base):
    __tablename__ = "appointment_feedback"
    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(Integer, ForeignKey('appointments.id'))
    rating = Column(Integer)
    comments = Column(Text)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    appointment_id = Column(Integer, ForeignKey('appointments.id'), nullable=True)
    notification_type = Column(Enum(NotificationType))
    status = Column(String)
    scheduled_send_time = Column(DateTime)

class SystemSettings(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True)
    value = Column(String)
    description = Column(Text)
