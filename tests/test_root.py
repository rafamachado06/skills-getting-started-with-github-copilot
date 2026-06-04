"""
Tests for the root endpoint (GET /)
"""
import pytest


def test_root_redirects_to_static_index(client):
    """Test that GET / redirects to the static index.html file"""
    # Arrange
    # No setup needed - just calling the root endpoint
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_follows_redirect_to_index(client):
    """Test that GET / can be followed and returns the index.html content"""
    # Arrange
    # No setup needed
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
    # The response should contain HTML content from index.html
    assert "text/html" in response.headers.get("content-type", "")
