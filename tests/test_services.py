from contextlib import asynccontextmanager
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import pytest
from api.main import app  # Import your FastAPI app
from api.models import Base, Availability  # Adjust imports as needed
from datetime import datetime
from api.dependencies import get_db  # Import your actual dependency

# Assuming your FastAPI app uses a dependency to provide a session
async def override_get_db():
    async_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async_session_local = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    async with async_session_local() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db  # Replace get_db with your actual dependency

@asynccontextmanager
async def client():
    async with TestClient(app) as c:
        yield c

@pytest.fixture
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)
    async_session_local = sessionmaker(engine, class_=AsyncSession)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session_local() as session:
        new_records = [
            Availability(provider_id=1, start_time=datetime(2022, 1, 1, 9, 0),
                         end_time=datetime(2022, 1, 1, 9, 30), status="Available"),
            Availability(provider_id=1, start_time=datetime(2022, 1, 1, 10, 0),
                         end_time=datetime(2022, 1, 1, 10, 30), status="Available")
        ]
        
        for record in new_records:
            session.add(record)
        await session.commit()

@pytest.mark.asyncio
async def test_get_available_appointments(client: TestClient, test_db):
    async with client() as c:
        response = client.get("/appointments/available")
        assert response.status_code == 200
        appointments = response.json()
        assert len(appointments) == 2
        assert appointments[0]["provider_id"] == 1
        assert appointments[1]["provider_id"] == 1
