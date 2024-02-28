from sqlalchemy.ext.asyncio import AsyncSession
from .models import Availability
from .schemas import AvailabilityBase  # Adjust import paths as needed

async def get_available_appointments(db: AsyncSession) -> list[AvailabilityBase]:
    query = await db.execute(select(Availability))
    return query.scalars().all()
