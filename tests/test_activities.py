"""
Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving activities."""

    def test_get_activities_returns_all_activities(self, test_client, reset_activities):
        """
        Test that GET /activities returns all available activities.
        
        AAA Pattern:
        - Arrange: Test client is ready
        - Act: Make GET request to /activities
        - Assert: Response contains all activities
        """
        # Arrange
        expected_activity_names = {
            "Chess Club", "Programming Class", "Gym Class",
            "Soccer Team", "Basketball Club", "Art Club",
            "Drama Club", "Debate Team", "Mathletes"
        }
        
        # Act
        response = test_client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert set(activities.keys()) == expected_activity_names

    def test_get_activities_returns_activity_structure(self, test_client, reset_activities):
        """
        Test that each activity has the required fields.
        
        AAA Pattern:
        - Arrange: Expected activity structure
        - Act: Get activities and check one
        - Assert: Verify structure contains required fields
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = test_client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert set(activity_data.keys()) == required_fields
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_get_activities_contains_participants(self, test_client, reset_activities):
        """
        Test that activities have the correct participants listed.
        
        AAA Pattern:
        - Arrange: Know expected participants for a specific activity
        - Act: Get activities
        - Assert: Verify participants are in the response
        """
        # Arrange
        expected_chess_club_participants = {"michael@mergington.edu", "daniel@mergington.edu"}
        
        # Act
        response = test_client.get("/activities")
        activities = response.json()
        
        # Assert
        chess_club = activities["Chess Club"]
        actual_participants = set(chess_club["participants"])
        assert actual_participants == expected_chess_club_participants
