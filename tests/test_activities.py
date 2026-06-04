"""
Tests for the activities endpoint (GET /activities)
"""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities in the database"""
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Basketball Club",
        "Art Club",
        "Drama Club",
        "Debate Team",
        "Science Club",
    ]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(activities) == len(expected_activities)
    for activity_name in expected_activities:
        assert activity_name in activities


def test_get_activities_returns_correct_structure(client):
    """Test that each activity has the required fields"""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict), f"{activity_name} should be a dict"
        assert required_fields == set(activity_data.keys()), \
            f"{activity_name} missing required fields"


def test_get_activities_has_correct_participant_format(client):
    """Test that participants are returned as a list of email strings"""
    # Arrange
    # No specific setup needed
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        participants = activity_data["participants"]
        assert isinstance(participants, list), \
            f"{activity_name} participants should be a list"
        for participant in participants:
            assert isinstance(participant, str), \
                f"Participant in {activity_name} should be a string (email)"
            assert "@" in participant, \
                f"Participant {participant} in {activity_name} should be an email"


def test_get_activities_has_positive_max_participants(client):
    """Test that max_participants values are positive integers"""
    # Arrange
    # No specific setup needed
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity_name, activity_data in activities.items():
        max_participants = activity_data["max_participants"]
        assert isinstance(max_participants, int), \
            f"{activity_name} max_participants should be an integer"
        assert max_participants > 0, \
            f"{activity_name} max_participants should be positive"
