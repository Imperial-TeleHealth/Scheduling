from fastapi import FastAPI, Depends, Body, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from . import services, schemas  # Assuming you have Pydantic schemas defined for request and response validation
from .dependencies import get_db  # Database session dependency

app = FastAPI()

# Patients
@app.get("/appointments/available", response_model=list[schemas.AvailabilityBase])
async def view_available_appointments(db: AsyncSession = Depends(get_db)):
    appointments = await services.get_available_appointments(db)
    return appointments

# view available appointments for a healthcare provider
@app.get("/appointments/available/{provider_id}", response_model=list[schemas.AvailabilityBase])
async def view_provider_available_appointments(provider_id: int, db: AsyncSession = Depends(get_db)):
    appointments = await services.get_provider_available_appointments(provider_id, db)
    return appointments

# view my patient's upcoming appointments
@app.get("/appointments/{patient_id}/upcoming", response_model=list[schemas.AppointmentBase])
async def view_patient_upcoming_appointments(patient_id: int, db: AsyncSession = Depends(get_db)):
    appointments = await services.get_patient_upcoming_appointments(patient_id, db)
    return appointments

# view upcoming appointments for a healthcare provider
@app.get("/appointments/{provider_id}/scheduled", response_model=list[schemas.AppointmentBase])
async def view_provider_scheduled_appointments(provider_id: int, db: AsyncSession = Depends(get_db)):
    appointments = await services.get_provider_scheduled_appointments(provider_id, db)
    return appointments

@app.post("/appointments/book", response_model=schemas.Appointment)
async def book_appointment(appointment: schemas.AppointmentCreate = Body(...), db: AsyncSession = Depends(get_db)):
    try:
        response = await services.book_appointment(appointment, db)
        return response
    except ValueError as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
 

@app.delete("/appointments/{appointment_id}/cancel")
async def cancel_appointment(appointment_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await services.cancel_appointment(appointment_id, db)
        return {"message": "Appointment cancelled successfully"}
    except ValueError as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))



@app.get("/patients/{patient_id}/appointments", response_model=list[schemas.Appointment])
async def view_patient_appointments(patient_id: int, db: AsyncSession = Depends(get_db)):
    appointments = await services.get_patient_appointments(patient_id, db)
    return appointments

@app.get("/providers/{provider_id}/appointments", response_model=list[schemas.Appointment])
async def view_provider_appointments(provider_id: int, db: AsyncSession = Depends(get_db)):
    appointments = await services.get_provider_appointments(provider_id, db)
    return appointments
