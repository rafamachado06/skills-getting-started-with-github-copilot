"""
Tests for the delete participant endpoint (DELETE /activities/{activity_name}/participants)
"""
import pytest


def test_delete_participant_successful_removes_from_activity(client, test_email):
    """Test that a participant can be successfully removed from an activity"""
    # Arrange
    activity_name = "Chess Club"
    
    # First, sign up the participant
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    activities_before = client.get("/activities").json()
    initial_count = len(activities_before[activity_name]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    assert test_email in response.json()["message"]
    
    activities_after = client.get("/activities").json()
    assert test_email not in activities_after[activity_name]["participants"]
    assert len(activities_after[activity_name]["participants"]) == initial_count - 1


def test_delete_nonexistent_participant_fails(client):
    """Test that removing a participant not in the activity returns 404"""
    # Arrange
    activity_name = "Basketball Club"
    email = "not.a.participant@example.com"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_from_nonexistent_activity_fails(client, test_email):
    """Test that deleting from a non-existent activity returns 404"""
    # Arrange
    activity_name = "Non-Existent Activity"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_delete_missing_email_parameter_fails(client):
    """Test that delete without email query parameter returns 422 validation error"""
    # Arrange
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/participants")
    
    # Assert
    assert response.status_code == 422
    assert "detail" in response.json()


def test_delete_participant_can_rejoin_activity(client, test_email):
    """Test that a removed participant can sign up again for the activity"""
    # Arrange
    activity_name = "Programming Class"
    
    # Sign up
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Remove
    response1 = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": test_email}
    )
    
    # Act - Re-sign up
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    activities = client.get("/activities").json()
    assert test_email in activities[activity_name]["participants"]


def test_delete_one_participant_does_not_affect_others(client, test_email, another_test_email):
    """Test that removing one participant doesn't affect other participants"""
    # Arrange
    activity_name = "Soccer Team"
    
    # Sign up two participants
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": another_test_email}
    )
    
    # Act - Remove first participant
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    
    activities = client.get("/activities").json()
    assert test_email not in activities[activity_name]["participants"]
    assert another_test_email in activities[activity_name]["participants"]


def test_delete_from_existing_activity_preserves_other_participants(client):
    """Test that removing a participant from activity with existing members works correctly"""
    # Arrange
    activity_name = "Drama Club"
    email_to_remove = "sara@mergington.edu"  # Pre-existing participant
    
    # Get initial state
    activities_before = client.get("/activities").json()
    initial_participants = activities_before[activity_name]["participants"].copy()
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email_to_remove}
    )
    
    # Assert
    assert response.status_code == 200
    
    activities_after = client.get("/activities").json()
    final_participants = activities_after[activity_name]["participants"]
    
    # Verify the specific participant was removed
    assert email_to_remove not in final_participants
    
    # Verify other participants remain
    for participant in initial_participants:
        if participant != email_to_remove:
            assert participant in final_participants
