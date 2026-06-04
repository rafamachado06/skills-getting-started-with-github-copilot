"""
Shared test fixtures and configuration for FastAPI tests.
"""
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture
def client():
    """
    Fixture providing a TestClient instance for testing FastAPI endpoints.
    
    Resets the in-memory activities database before each test to ensure
    test isolation and prevent state leakage between tests.
    """
    # Reset the activities database to initial state
    app_module.activities.clear()
    app_module.activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Competitive soccer team training and matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["alex@mergington.edu", "maria@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Pickup games and skill development for basketball",
            "schedule": "Wednesdays and Fridays, 4:30 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["kevin@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and mixed media projects",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["linda@mergington.edu", "noah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting workshops and school theater productions",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 30,
            "participants": ["sara@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate practice and tournaments",
            "schedule": "Tuesdays, 5:00 PM - 6:30 PM",
            "max_participants": 16,
            "participants": ["ryan@mergington.edu", "zoe@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and science fair projects",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 22,
            "participants": ["lucas@mergington.edu"]
        }
    })
    
    return TestClient(app_module.app)


@pytest.fixture
def test_email():
    """
    Fixture providing a standard test email address for signup and deletion tests.
    """
    return "test.student@example.com"


@pytest.fixture
def another_test_email():
    """
    Fixture providing a second test email address for multi-student scenarios.
    """
    return "another.student@example.com"
