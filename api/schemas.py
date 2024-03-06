from pydantic import BaseModel, ConfigDict, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
import enum

# Enum Definitions
class Role(str, enum.Enum):
    patient = "Patient"
    healthcare_provider = "Healthcare Provider"
    administrator = "Administrator"

class Status(str, enum.Enum):
    available = "Available"
    booked = "Booked"
    cancelled = "Cancelled"
    blocked = "Blocked"

class NotificationType(str, enum.Enum):
    appointment_reminder = "AppointmentReminder"
    appointment_change = "AppointmentChange"

class AppointmentStatus(str, enum.Enum):
    scheduled = "Scheduled"
    completed = "Completed"
    cancelled = "Cancelled"
    no_show = "NoShow"

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    role: Role

class UserCreate(UserBase):
    password: str

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    
    
# HealthcareProvider Schemas
class HealthcareProviderBase(BaseModel):
    user_id: int

class HealthcareProviderCreate(HealthcareProviderBase):
    pass

class HealthcareProvider(HealthcareProviderBase):
    model_config = ConfigDict(from_attributes=True)
    id: int



# Patient Schemas
class PatientBase(BaseModel):
    user_id: int


class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    model_config = ConfigDict(from_attributes=True)
    id: int



# Availability Schemas
class AvailabilityBase(BaseModel):
    provider_id: int
    start_time: datetime
    end_time: datetime
    status: Status

class AvailabilityCreate(AvailabilityBase):
    pass

class Availability(AvailabilityBase):
    model_config = ConfigDict(from_attributes=True)
    id: int



# Appointment Schemas
class AppointmentBase(BaseModel):
    patient_id: int
    provider_id: int
    scheduled_time: datetime
    end_time: datetime
    reason_for_visit: str
    status: AppointmentStatus
    video_link: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    model_config = ConfigDict(from_attributes=True)
    id: int



# AppointmentFeedback Schemas
class AppointmentFeedbackBase(BaseModel):
    appointment_id: int
    rating: int = Field(ge=1, le=5)
    comments: Optional[str] = None

class AppointmentFeedbackCreate(AppointmentFeedbackBase):
    pass

class AppointmentFeedback(AppointmentFeedbackBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# Notification Schemas
class NotificationBase(BaseModel):
    user_id: int
    appointment_id: Optional[int] = None
    notification_type: NotificationType
    status: str
    scheduled_send_time: datetime

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int



# SystemSettings Schemas
class SystemSettingsBase(BaseModel):
    key: str
    value: str
    description: Optional[str] = None

class SystemSettingsCreate(SystemSettingsBase):
    pass

class SystemSettings(SystemSettingsBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


