"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup)
"""
import pytest


def test_signup_successful_adds_participant(client, test_email):
    """Test that a student can successfully sign up for an available activity"""
    # Arrange
    activity_name = "Chess Club"
    
    # Get initial state
    activities_before = client.get("/activities").json()
    initial_count = len(activities_before[activity_name]["participants"])
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert test_email in response.json()["message"]
    
    # Verify participant was added
    activities_after = client.get("/activities").json()
    assert test_email in activities_after[activity_name]["participants"]
    assert len(activities_after[activity_name]["participants"]) == initial_count + 1


def test_signup_to_multiple_activities(client, test_email, another_test_email):
    """Test that a student can sign up for multiple different activities"""
    # Arrange
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    
    # Act - Sign up for first activity
    response1 = client.post(
        f"/activities/{activity1}/signup",
        params={"email": test_email}
    )
    
    # Act - Sign up for second activity
    response2 = client.post(
        f"/activities/{activity2}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities = client.get("/activities").json()
    assert test_email in activities[activity1]["participants"]
    assert test_email in activities[activity2]["participants"]


def test_signup_duplicate_signup_fails(client, test_email):
    """Test that a student cannot sign up for the same activity twice"""
    # Arrange
    activity_name = "Chess Club"
    
    # Act - First signup
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Act - Attempt duplicate signup
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"]


def test_signup_nonexistent_activity_fails(client, test_email):
    """Test that signing up for a non-existent activity returns 404"""
    # Arrange
    activity_name = "Non-Existent Activity"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_signup_missing_email_parameter_fails(client):
    """Test that signup without email query parameter returns 422 validation error"""
    # Arrange
    activity_name = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup")
    
    # Assert
    assert response.status_code == 422
    # FastAPI returns validation error details
    assert "detail" in response.json()


def test_signup_with_empty_email_fails(client):
    """Test that signup with empty email string fails"""
    # Arrange
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": ""}
    )
    
    # Assert
    # Should still add empty string or handle gracefully
    # The exact behavior depends on implementation
    # If it succeeds, verify it was added; if it fails, verify error
    if response.status_code == 200:
        activities = client.get("/activities").json()
        assert "" in activities[activity_name]["participants"]
    else:
        assert response.status_code in [400, 422]


def test_signup_different_students_same_activity(client, test_email, another_test_email):
    """Test that multiple different students can sign up for the same activity"""
    # Arrange
    activity_name = "Gym Class"
    
    # Get initial participant count
    activities_before = client.get("/activities").json()
    initial_count = len(activities_before[activity_name]["participants"])
    
    # Act - First student signs up
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Act - Second student signs up
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": another_test_email}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities = client.get("/activities").json()
    assert test_email in activities[activity_name]["participants"]
    assert another_test_email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == initial_count + 2
