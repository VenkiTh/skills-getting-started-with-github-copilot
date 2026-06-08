"""Tests for POST /activities/{activity}/unregister endpoint using AAA pattern"""


def test_unregister_success(client):
    """Test successful unregister from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered" in data["message"]
    assert email in data["message"]


def test_unregister_activity_not_found(client):
    """Test unregister fails when activity does not exist"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_not_registered(client):
    """Test unregister fails when student is not registered"""
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "not registered" in data["detail"].lower()


def test_unregister_removes_participant_from_activity(client):
    """Test that unregister actually removes the participant from the activity"""
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"  # Already signed up

    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    activities = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
