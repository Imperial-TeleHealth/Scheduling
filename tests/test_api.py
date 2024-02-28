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
        {"id": 1, "provider_id": 1, "start_time": "2022-01-01T09:00:00", "end_time": "2022-01-01T09:30:00", "status": "Available"},
        {"id": 2, "provider_id": 1, "start_time": "2022-01-01T10:00:00", "end_time": "2022-01-01T10:30:00", "status": "Available"}
    ]

    with patch('api.services.get_available_appointments', return_value=mock_return_value):
        async with LifespanManager(app):
            # async with AsyncClient(app=app, base_url="http://test") as client:
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                response = await client.get("/appointments/available")
                assert response.status_code == 200
                assert response.json() == mock_return_value
