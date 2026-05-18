"""
Integration tests for FastAPI endpoints.

These tests validate the HTTP endpoints using FastAPI's TestClient.
All tests follow the AAA pattern:
- Arrange: Set up the test client and any required data
- Act: Make HTTP requests to the endpoints
- Assert: Verify the response status codes and data
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Create a TestClient for the FastAPI app."""
    return TestClient(app)


class TestRootEndpoint:
    """Test the root endpoint that redirects to the static files."""

    def test_root_redirects_to_index_html(self, client):
        """Test that GET / redirects to /static/index.html."""
        # Arrange
        # (client fixture is automatically provided)

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers.get("location", "")


class TestGetActivitiesEndpoint:
    """Test the GET /activities endpoint."""

    def test_get_all_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary of all activities."""
        # Arrange
        # (client fixture is automatically provided)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities_data = response.json()
        assert isinstance(activities_data, dict)

    def test_get_activities_contains_expected_activities(self, client):
        """Test that the response includes all expected activities."""
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Music Ensemble",
            "Debate Club",
            "Science Club"
        ]

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        for activity_name in expected_activities:
            assert activity_name in activities_data

    def test_activity_has_required_fields(self, client):
        """Test that each activity has all required fields."""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        for activity_name, activity_info in activities_data.items():
            for field in required_fields:
                assert field in activity_info, f"Activity '{activity_name}' missing field '{field}'"

    def test_participants_is_list(self, client):
        """Test that the participants field is a list."""
        # Arrange
        # (client fixture is automatically provided)

        # Act
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_info["participants"], list), \
                f"Activity '{activity_name}' participants is not a list"


class TestSignupEndpoint:
    """Test the POST /activities/{activity_name}/signup endpoint."""

    def test_successful_signup_for_activity(self, client):
        """Test successfully signing up a new participant for an activity."""
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
        response_data = response.json()
        assert "message" in response_data
        assert email in response_data["message"]
        assert activity_name in response_data["message"]

    def test_successful_signup_returns_confirmation_message(self, client):
        """Test that the signup response contains the correct confirmation message."""
        # Arrange
        activity_name = "Programming Class"
        email = "alice@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        message = response.json()["message"]

        # Assert
        assert "Signed up" in message
        assert email in message
        assert activity_name in message

    def test_signup_adds_participant_to_activity(self, client):
        """Test that after signup, the participant appears in the activity's participant list."""
        # Arrange
        activity_name = "Art Studio"
        email = "bob@mergington.edu"

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        assert email in activities_data[activity_name]["participants"]


class TestRemoveParticipantEndpoint:
    """Test the DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_successful_removal_of_existing_participant(self, client):
        """Test successfully removing an existing participant from an activity."""
        # Arrange
        activity_name = "Tennis Club"
        email = "ryan@mergington.edu"  # Known participant from initial data

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert email in response_data["message"]
        assert activity_name in response_data["message"]

    def test_removal_returns_confirmation_message(self, client):
        """Test that the removal response contains the correct confirmation message."""
        # Arrange
        activity_name = "Music Ensemble"
        email = "maya@mergington.edu"  # Known participant from initial data

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        message = response.json()["message"]

        # Assert
        assert "Removed" in message
        assert email in message
        assert activity_name in message

    def test_removal_removes_participant_from_activity(self, client):
        """Test that after removal, the participant is gone from the activity's participant list."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Known participant from initial data

        # Act
        client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )
        response = client.get("/activities")
        activities_data = response.json()

        # Assert
        assert email not in activities_data[activity_name]["participants"]
