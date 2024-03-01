from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api import models, schemas
from datetime import datetime

async def get_available_appointments(db: AsyncSession) -> list[schemas.AvailabilityBase]:
    query = await db.execute(select(models.Availability))
    return query.scalars().all()


# get patient's upcoming appointments after the current time
async def get_patient_upcoming_appointments(patient_id: int, current_time: datetime, db: AsyncSession) -> list[schemas.AppointmentBase]:
    query = await db.execute(select(models.Appointment).where(models.Appointment.patient_id == patient_id).where(models.Appointment.scheduled_time > current_time))
    return query.scalars().all()



