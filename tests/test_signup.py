"""Tests for POST /activities/{activity}/signup endpoint using AAA pattern"""


def test_signup_success(client):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up" in data["message"]
    assert email in data["message"]


def test_signup_activity_not_found(client):
    """Test signup fails when activity does not exist"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_already_registered(client):
    """Test signup fails when student is already registered"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up for Chess Club

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"].lower()


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity"""
    # Arrange
    activity_name = "Programming Class"
    email = "test_student_unique@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    activities = activities_response.json()

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
