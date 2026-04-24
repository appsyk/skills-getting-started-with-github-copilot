"""
Pytest configuration and fixtures for API tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def test_client():
    """Provide a FastAPI TestClient for making requests."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Reset activities to a known state before each test.
    This ensures test isolation and prevents test pollution.
    """
    # Store original state
    original_activities = {
        key: {
            "description": value["description"],
            "schedule": value["schedule"],
            "max_participants": value["max_participants"],
            "participants": value["participants"].copy(),
        }
        for key, value in activities.items()
    }
    
    yield
    
    # Restore original state after test
    for key in activities:
        activities[key]["participants"] = original_activities[key]["participants"].copy()
