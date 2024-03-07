from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api import models, schemas
from datetime import datetime

async def get_available_appointments(db: AsyncSession) -> list[schemas.AvailabilityBase]:
    async with db as session:
        result = await session.execute(select(models.Availability).where(models.Availability.start_time > datetime.today()))
        return result.scalars().all()

# get available appointments for a healthcare provider after the current time
async def get_provider_available_appointments(provider_id: int, db: AsyncSession) -> list[schemas.AvailabilityBase]:
    async with db as session:
        result = await session.execute(select(models.Availability).where(models.Availability.provider_id == provider_id).where(models.Availability.start_time > datetime.today()))
        return result.scalars().all()
# get patient's upcoming appointments after the current time
async def get_patient_upcoming_appointments(patient_id: int, db: AsyncSession) -> list[schemas.AppointmentBase]:
    async with db as session:
        result = await session.execute(select(models.Appointment).where(models.Appointment.patient_id == patient_id).where(models.Appointment.end_time > datetime.now()))
        return result.scalars().all()

# get upcoming appointments for a healthcare provider after the current time
async def get_provider_scheduled_appointments(provider_id: int, db: AsyncSession) -> list[schemas.AppointmentBase]:
    async with db as session:
        result = await session.execute(select(models.Appointment).where(models.Appointment.provider_id == provider_id).where(models.Appointment.end_time > datetime.now()))
        return result.scalars().all()


# book an appointment
async def book_appointment(appointment: schemas.AppointmentCreate, db: AsyncSession) -> schemas.Appointment:
    async with db as session:
        # check if the appointment slot is available
        appointment_start = appointment.scheduled_time
        provider_id = appointment.provider_id
        result = await session.execute(select(models.Availability).where(models.Availability.provider_id == provider_id).where(models.Availability.start_time == appointment_start))
        availability = result.scalars().first()
        if availability.status != models.Status.available:
            raise ValueError("Appointment slot is not available")
        
        # generate video link
        video_link = f"https://example.com/video/{appointment.scheduled_time}"
        
        appointment_data = appointment.dict()
        appointment_data["video_link"] = video_link
        db_appointment = models.Appointment(**appointment_data, status=models.AppointmentStatus.scheduled)
        session.add(db_appointment)
        session.commit()
        session.refresh(db_appointment)
        # update availability status for healthcare provider
        availability.status = models.Status.booked
        session.commit()
        
        return db_appointment

# cancel an appointment
async def cancel_appointment(appointment_id: int, db: AsyncSession):
    async with db as session:
        query = await session.execute(select(models.Appointment).where(models.Appointment.id == appointment_id))
        appointment = query.scalars().first()
        if appointment.status != models.AppointmentStatus.scheduled:
            raise ValueError("Appointment cannot be cancelled")
        appointment.status = models.AppointmentStatus.cancelled
        session.commit()
        # update availability status for healthcare provider
        query = await session.execute(select(models.Availability).where(models.Availability.provider_id == appointment.provider_id).where(models.Availability.start_time == appointment.scheduled_time))
        availability = query.scalars().first()
        availability.status = models.Status.available
        session.commit()
        return {"message": "Appointment cancelled successfully"}

# get patient's appointments
async def get_patient_appointments(patient_id: int, db: AsyncSession) -> list[schemas.Appointment]:
    async with db as session:
        result = await session.execute(select(models.Appointment).where(models.Appointment.patient_id == patient_id))
        return result.scalars().all()

# get healthcare provider's appointments
async def get_provider_appointments(provider_id: int, db: AsyncSession) -> list[schemas.Appointment]:
    async with db as session:
        query = await session.execute(select(models.Appointment).where(models.Appointment.provider_id == provider_id))
        return query.scalars().all()


