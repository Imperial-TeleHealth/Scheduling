import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from asgi_lifespan import LifespanManager
import os
from unittest.mock import patch

# Ensure all tests automatically use this fixture, setting the DATABASE_URL
@pytest.fixture(autouse=True)
def setup_test_environment():
    # Set up the environment variable for the test
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
    print(os.getenv("DATABASE_URL"))
    yield  # Provide control back to the test case



@pytest.mark.asyncio
async def test_view_available_appointments():
    # Import the FastAPI app after setting up the test environment fixture
    from api.main import app
    mock_return_value = [
        { "provider_id": "1", "start_time": "2022-01-01T09:00:00", "end_time": "2022-01-01T09:30:00", "status": "Available"},
        { "provider_id": "1", "start_time": "2022-01-01T10:00:00", "end_time": "2022-01-01T10:30:00", "status": "Available"}
    ]

    with patch('api.services.get_available_appointments', return_value=mock_return_value):
        async with LifespanManager(app):
            # async with AsyncClient(app=app, base_url="http://test") as client:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/appointments/available")
                assert response.status_code == 200
                assert response.json() == mock_return_value


# view my upcoming appointments
@pytest.mark.asyncio
async def test_view_patient_upcoming_appointments():
    # Import the FastAPI app after setting up the test environment fixture
    from api.main import app

    mock_return_value = [
        {"patient_id": "1" , "provider_id": "1", "scheduled_time": "2022-01-01T09:00:00", "end_time": "2022-01-01T09:30:00",  "reason_for_visit": "Annual checkup" },
        {"patient_id": "1" , "provider_id": "2", "scheduled_time": "2022-02-01T10:00:00", "end_time": "2022-02-01T10:30:00",  "reason_for_visit": "Follow Up" }
    ]

    with patch('api.services.get_patient_upcoming_appointments', return_value=mock_return_value):
        async with LifespanManager(app):
            # async with AsyncClient(app=app, base_url="http://test") as client:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/appointments/1/upcoming")
                assert response.status_code == 200
                assert response.json() == mock_return_value

# view my upcoming appointments
@pytest.mark.asyncio
async def test_view_provider_upcoming_appointments():
    # Import the FastAPI app after setting up the test environment fixture
    from api.main import app

    mock_return_value = [
        {"patient_id": "1" , "provider_id": "1", "scheduled_time": "2022-01-01T09:00:00", "end_time": "2022-01-01T09:30:00",  "reason_for_visit": "Annual checkup" },
        {"patient_id": "2" , "provider_id": "1", "scheduled_time": "2022-02-01T10:00:00", "end_time": "2022-02-01T10:30:00",  "reason_for_visit": "Follow Up" }
    ]

    with patch('api.services.get_provider_scheduled_appointments', return_value=mock_return_value):
        async with LifespanManager(app):
            # async with AsyncClient(app=app, base_url="http://test") as client:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/appointments/1/scheduled")
                assert response.status_code == 200
                assert response.json() == mock_return_value


@pytest.mark.asyncio
async def test_book_appointment():
    # Import the FastAPI app after setting up the test environment fixture
    from api.main import app
    mock_return_value = {"id": 1,"patient_id": "1", "provider_id": "1", "scheduled_time": "2022-01-01T09:00:00", "end_time": "2022-01-01T09:30:00", "status": "Scheduled", "reason_for_visit": "Annual checkup", "video_link": "https://example.com/video/2022-01-01T09:00:00"}

    with patch('api.services.book_appointment', return_value=mock_return_value):
        async with LifespanManager(app):
            # async with AsyncClient(app=app, base_url="http://test") as client:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.post("/appointments/book", json={"patient_id": "1", "provider_id": "1", "scheduled_time": "2022-01-01T09:00:00", "end_time": "2022-01-01T09:30:00", "reason_for_visit": "Annual checkup"})
                assert response.status_code == 200, response.json()
                assert response.json() == mock_return_value

@pytest.mark.asyncio
async def test_cancel_appointment():
    # Import the FastAPI app after setting up the test environment fixture
    from api.main import app
    mock_return_value = {"message": "Appointment cancelled successfully"}

    with patch('api.services.cancel_appointment', return_value=mock_return_value):
        async with LifespanManager(app):
            # async with AsyncClient(app=app, base_url="http://test") as client:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.delete("/appointments/1/cancel")
                assert response.status_code == 200
                assert response.json() == mock_return_value


@pytest.mark.asyncio
async def test_view_patient_appointments():
    # Import the FastAPI app after setting up the test environment fixture
    from api.main import app
    mock_return_value = [
        {"id": 1, "patient_id": "1", "provider_id": "1", "scheduled_time": "2022-01-01T09:00:00", "end_time": "2022-01-01T09:30:00", "status": "Scheduled", "reason_for_visit": "Annual checkup", "video_link": "https://example.com/video/2022-01-01T09:00:00"},
        {"id": 2, "patient_id": "1", "provider_id": "2", "scheduled_time": "2022-01-01T10:00:00", "end_time": "2022-01-01T10:30:00", "status": "Scheduled", "reason_for_visit": "Follow Up", "video_link": "https://example.com/video/2022-01-01T10:00:00"}
    ]

    with patch('api.services.get_patient_appointments', return_value=mock_return_value):
        async with LifespanManager(app):
            # async with AsyncClient(app=app, base_url="http://test") as client:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/patients/1/appointments")
                assert response.status_code == 200
                assert response.json() == mock_return_value

@pytest.mark.asyncio
async def test_view_provider_appointments():
    # Import the FastAPI app after setting up the test environment fixture
    from api.main import app
    mock_return_value = [
        {"id": 1, "patient_id": "1", "provider_id": "1", "scheduled_time": "2022-01-01T09:00:00", "end_time": "2022-01-01T09:30:00", "status": "Scheduled", "reason_for_visit": "Annual checkup", "video_link": "https://example.com/video/2022-01-01T09:00:00"},
        {"id": 2, "patient_id": "2", "provider_id": "1", "scheduled_time": "2022-01-01T10:00:00", "end_time": "2022-01-01T10:30:00", "status": "Scheduled", "reason_for_visit": "Follow Up", "video_link": "https://example.com/video/2022-01-01T10:00:00"}
    ]

    with patch('api.services.get_provider_appointments', return_value=mock_return_value):
        async with LifespanManager(app):
            # async with AsyncClient(app=app, base_url="http://test") as client:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/providers/1/appointments")
                assert response.status_code == 200
                assert response.json() == mock_return_value

@pytest.mark.asyncio
async def test_cancel_appointment():
    # Import the FastAPI app after setting up the test environment fixture
    from api.main import app
    mock_return_value = {"message": "Appointment cancelled successfully"}

    with patch('api.services.cancel_appointment', return_value=mock_return_value):
        async with LifespanManager(app):
            # async with AsyncClient(app=app, base_url="http://test") as client:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.delete("/appointments/1/cancel")
                assert response.status_code == 200
                assert response.json() == mock_return_value