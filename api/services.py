from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api import models, schemas
from datetime import datetime

async def get_available_appointments(db: AsyncSession) -> list[schemas.AvailabilityBase]:
    async with db as session:
        result = await session.execute(select(models.Availability).where(models.Availability.start_time > datetime.today()))
        return result.scalars().all()

# get available appointments for a healthcare provider after the current time
async def get_provider_available_appointments(provider_id: str, db: AsyncSession) -> list[schemas.AvailabilityBase]:
    async with db as session:
        result = await session.execute(select(models.Availability).where(models.Availability.provider_id == provider_id).where(models.Availability.status == models.Status.available).where(models.Availability.start_time > datetime.today()))
        return result.scalars().all()
# get patient's upcoming appointments after the current time
async def get_patient_upcoming_appointments(patient_id: str, db: AsyncSession) -> list[schemas.AppointmentBase]:
    async with db as session:
        result = await session.execute(select(models.Appointment).where(models.Appointment.patient_id == patient_id).where(models.Appointment.end_time > datetime.now()))
        return result.scalars().all()
    
async def get_provider_upcoming_appointments(provider_id: str, db: AsyncSession) -> list[schemas.AppointmentBase]:
    async with db as session:
        result = await session.execute(select(models.Appointment).where(models.Appointment.provider_id == provider_id).where(models.Appointment.end_time > datetime.now()))
        return result.scalars().all()

# get upcoming appointments for a healthcare provider after the current time
async def get_provider_scheduled_appointments(provider_id: str, db: AsyncSession) -> list[schemas.AppointmentBase]:
    async with db as session:
        result = await session.execute(select(models.Appointment).where(models.Appointment.provider_id == provider_id).where(models.Appointment.end_time > datetime.now()))
        return result.scalars().all()


async def book_appointment(appointment: schemas.AppointmentCreate, db: AsyncSession) -> schemas.Appointment:
    async with db.begin():  # This starts a transaction.
        # Check if the appointment slot is available.
        result = await db.execute(select(models.Availability)
                                  .where(models.Availability.provider_id == appointment.provider_id)
                                  .where(models.Availability.start_time == appointment.scheduled_time)
                                  .where(models.Availability.status == models.Status.available))
        availability = result.scalars().first()
        if availability is None:
            raise ValueError("Appointment slot is not available")

        # Generate video link.
        video_link = f"https://example.com/video/{appointment.scheduled_time}"

        # Create appointment data and object.
        appointment_data = {
            "scheduled_time": appointment.scheduled_time,
            "end_time": appointment.end_time,
            "reason_for_visit": appointment.reason_for_visit,
            "patient_id": appointment.patient_id,
            "provider_id": appointment.provider_id,
            "video_link": video_link,
            "status": models.AppointmentStatus.scheduled
        }
        db_appointment = models.Appointment(**appointment_data)
        db.add(db_appointment)

        # Update availability status for healthcare provider.
        availability.status = models.Status.booked

        # The transaction will be committed at the end of the async with block.
        # If an exception occurs, it will be rolled back automatically.

    await db.refresh(db_appointment)  # Refresh to get the updated state from the DB.
    
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
async def get_patient_appointments(patient_id: str, db: AsyncSession) -> list[schemas.Appointment]:
    async with db as session:
        result = await session.execute(select(models.Appointment).where(models.Appointment.patient_id == patient_id))
        return result.scalars().all()

# get healthcare provider's appointments
async def get_provider_appointments(provider_id: str, db: AsyncSession) -> list[schemas.Appointment]:
    async with db as session:
        query = await session.execute(select(models.Appointment).where(models.Appointment.provider_id == provider_id))
        return query.scalars().all()


