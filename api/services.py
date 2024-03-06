from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api import models, schemas
from datetime import datetime

async def get_available_appointments(db: AsyncSession) -> list[schemas.AvailabilityBase]:
    query = await db.execute(select(models.Availability)).where(models.Availability.start_time > datetime.today())
    return query.scalars().all()

# get available appointments for a healthcare provider after the current time
async def get_provider_available_appointments(provider_id: int, db: AsyncSession) -> list[schemas.AvailabilityBase]:
    query = await db.execute(select(models.Availability).where(models.Availability.provider_id == provider_id).where(models.Availability.start_time > datetime.today()))
    return query.scalars().all()

# get patient's upcoming appointments after the current time
async def get_patient_upcoming_appointments(patient_id: int, current_time: datetime, db: AsyncSession) -> list[schemas.AppointmentBase]:
    query = await db.execute(select(models.Appointment).where(models.Appointment.patient_id == patient_id).where(models.Appointment.end_time > datetime.now()))
    return query.scalars().all()

# get upcoming appointments for a healthcare provider after the current time
async def get_provider_scheduled_appointments(provider_id: int, db: AsyncSession) -> list[schemas.AppointmentBase]:
    query = await db.execute(select(models.Appointment).where(models.Appointment.provider_id == provider_id).where(models.Appointment.end_time > datetime.now()))
    return query.scalars().all()

# book an appointment
async def book_appointment(appointment: schemas.AppointmentCreate, db: AsyncSession) -> schemas.Appointment:
    # check if the appointment slot is available
    appointment_start = appointment.scheduled_time
    provider_id = appointment.provider_id
    query = await db.execute(select(models.Availability).where(models.Availability.provider_id == provider_id).where(models.Availability.start_time == appointment_start))
    availability = query.scalars().first()
    if availability is not models.Status.available:
        raise ValueError("Appointment slot is not available")
    
    # generate video link
    appointment.video_link = f"https://example.com/video/{appointment.scheduled_time}" # this should be generated by a video call service
    

    db_appointment = models.Appointment(**appointment.model_dump(), status=models.AppointmentStatus.scheduled, video_link=appointment.video_link)
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    # update availability status for healthcare provider
    availability.status = models.Status.booked
    await db.commit()


    return db_appointment

# book an appointment
async def book_appointment(appointment: schemas.AppointmentCreate, db: AsyncSession) -> schemas.Appointment:
    # check if the appointment slot is available
    appointment_start = appointment.scheduled_time
    provider_id = appointment.provider_id
    query = await db.execute(select(models.Availability).where(models.Availability.provider_id == provider_id).where(models.Availability.start_time == appointment_start))
    availability = query.scalars().first()
    if availability.status != models.Status.available:
        raise ValueError("Appointment slot is not available")
    
    # generate video link
    video_link = f"https://example.com/video/{appointment.scheduled_time}"
    
    appointment_data = appointment.model_dump()
    appointment_data["video_link"] = video_link
    db_appointment = models.Appointment(**appointment_data, status=models.AppointmentStatus.scheduled)
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    # update availability status for healthcare provider
    availability.status = models.Status.booked
    db.commit()
    
    return db_appointment

# cancel an appointment
async def cancel_appointment(appointment_id: int, db: AsyncSession):
    query = await db.execute(select(models.Appointment).where(models.Appointment.id == appointment_id))
    appointment = query.scalars().first()
    if appointment.status != models.AppointmentStatus.scheduled:
        raise ValueError("Appointment cannot be cancelled")
    appointment.status = models.AppointmentStatus.cancelled
    db.commit()
    # update availability status for healthcare provider
    query = await db.execute(select(models.Availability).where(models.Availability.provider_id == appointment.provider_id).where(models.Availability.start_time == appointment.scheduled_time))
    availability = query.scalars().first()
    availability.status = models.Status.available
    db.commit()
    return {"message": "Appointment cancelled successfully"}

# get patient's appointments
async def get_patient_appointments(patient_id: int, db: AsyncSession) -> list[schemas.Appointment]:
    query = await db.execute(select(models.Appointment).where(models.Appointment.patient_id == patient_id))
    return query.scalars().all()

# get healthcare provider's appointments
async def get_provider_appointments(provider_id: int, db: AsyncSession) -> list[schemas.Appointment]:
    query = await db.execute(select(models.Appointment).where(models.Appointment.provider_id == provider_id))
    return query.scalars().all()


