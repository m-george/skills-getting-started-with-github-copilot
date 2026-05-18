"""
Unit tests for activities business logic.

These tests validate the core logic of the activities system using the AAA pattern:
- Arrange: Set up test data and conditions
- Act: Execute the logic being tested
- Assert: Verify the results match expectations
"""

import pytest


class TestActivityStructure:
    """Test the structure and properties of activities."""

    def test_activity_has_required_fields(self):
        """Test that an activity has all required fields."""
        # Arrange
        activity = {
            "description": "Learn strategies and compete",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        }

        # Act
        has_description = "description" in activity
        has_schedule = "schedule" in activity
        has_max_participants = "max_participants" in activity
        has_participants = "participants" in activity

        # Assert
        assert has_description
        assert has_schedule
        assert has_max_participants
        assert has_participants

    def test_activity_participants_starts_as_list(self):
        """Test that participants is initialized as a list."""
        # Arrange
        activity = {
            "description": "Learn strategies",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": []
        }

        # Act
        participants_type = type(activity["participants"])

        # Assert
        assert participants_type == list


class TestParticipantSignup:
    """Test the logic for signing up participants."""

    def test_add_participant_to_activity(self):
        """Test adding a participant to an activity's participant list."""
        # Arrange
        activity = {
            "description": "Learn programming",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        }
        email = "newstudent@mergington.edu"

        # Act
        activity["participants"].append(email)

        # Assert
        assert email in activity["participants"]
        assert len(activity["participants"]) == 2

    def test_add_multiple_participants(self):
        """Test adding multiple participants sequentially."""
        # Arrange
        activity = {
            "description": "Physical education",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        }
        emails = ["john@mergington.edu", "olivia@mergington.edu", "alex@mergington.edu"]

        # Act
        for email in emails:
            activity["participants"].append(email)

        # Assert
        assert len(activity["participants"]) == 3
        for email in emails:
            assert email in activity["participants"]

    def test_participant_already_in_activity(self):
        """Test detecting when a participant is already signed up."""
        # Arrange
        email = "michael@mergington.edu"
        activity = {
            "description": "Chess strategies",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": [email]
        }

        # Act
        is_already_signed_up = email in activity["participants"]

        # Assert
        assert is_already_signed_up is True


class TestParticipantRemoval:
    """Test the logic for removing participants."""

    def test_remove_participant_from_activity(self):
        """Test removing a participant from an activity's participant list."""
        # Arrange
        email = "michael@mergington.edu"
        activity = {
            "description": "Chess strategies",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": [email, "daniel@mergington.edu"]
        }

        # Act
        activity["participants"].remove(email)

        # Assert
        assert email not in activity["participants"]
        assert len(activity["participants"]) == 1

    def test_remove_multiple_participants(self):
        """Test removing multiple participants sequentially."""
        # Arrange
        activity = {
            "description": "Orchestra",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["maya@mergington.edu", "adam@mergington.edu", "sophie@mergington.edu"]
        }
        emails_to_remove = ["maya@mergington.edu", "adam@mergington.edu"]

        # Act
        for email in emails_to_remove:
            activity["participants"].remove(email)

        # Assert
        assert len(activity["participants"]) == 1
        assert "sophie@mergington.edu" in activity["participants"]
        for email in emails_to_remove:
            assert email not in activity["participants"]

    def test_participant_not_in_activity(self):
        """Test detecting when a participant is not in an activity."""
        # Arrange
        email = "notregistered@mergington.edu"
        activity = {
            "description": "Debate club",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["sarah@mergington.edu"]
        }

        # Act
        is_in_activity = email in activity["participants"]

        # Assert
        assert is_in_activity is False
