"""Tests for GET /activities endpoint using AAA pattern"""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities"""
    # Arrange
    expected_activity_names = ["Chess Club", "Programming Class", "Gym Class",
                               "Soccer Team", "Basketball Club", "Art Workshop",
                               "Drama Club", "Math Olympiad", "Science Club"]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    for activity_name in expected_activity_names:
        assert activity_name in activities


def test_get_activities_returns_activity_structure(client):
    """Test that activities have the correct structure"""
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Activity {activity_name} missing field: {field}"


def test_get_activities_participants_is_list(client):
    """Test that participants field is a list"""
    # Arrange
    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["participants"], list)


def test_get_activities_max_participants_is_number(client):
    """Test that max_participants is a number"""
    # Arrange
    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["max_participants"], int)
        assert activity_data["max_participants"] > 0
