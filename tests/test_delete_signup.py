"""
Tests for DELETE /activities/{activity_name}/signup endpoint using AAA pattern.
"""

import pytest


class TestDeleteSignup:
    """Test suite for activity unregistration (delete signup) functionality."""

    def test_delete_signup_removes_participant(self, test_client, reset_activities):
        """
        Test that a student can successfully unregister from an activity.
        
        AAA Pattern:
        - Arrange: Get initial participant list
        - Act: Send DELETE request to unregister
        - Assert: Participant is removed from activity
        """
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"
        initial_response = test_client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        response = test_client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "unregistered" in result["message"].lower() or "unregister" in result["message"].lower()
        
        # Verify participant was actually removed
        updated_response = test_client.get("/activities")
        updated_participants = updated_response.json()[activity_name]["participants"]
        assert len(updated_participants) == initial_count - 1
        assert email not in updated_participants

    def test_delete_signup_nonexistent_activity_returns_404(self, test_client, reset_activities):
        """
        Test that unregistering from a non-existent activity returns 404.
        
        AAA Pattern:
        - Arrange: Prepare request with invalid activity name
        - Act: Send DELETE request
        - Assert: Response is 404
        """
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = test_client.delete(
            f"/activities/{nonexistent_activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "not found" in result["detail"].lower()

    def test_delete_signup_student_not_signed_up_returns_400(self, test_client, reset_activities):
        """
        Test that attempting to unregister a student not in the activity returns 400.
        
        AAA Pattern:
        - Arrange: Prepare email of student not in activity
        - Act: Send DELETE request
        - Assert: Response is 400 with appropriate error message
        """
        # Arrange
        email = "notstudent@mergington.edu"
        activity_name = "Chess Club"
        
        # Act
        response = test_client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "not signed up" in result["detail"].lower()

    def test_delete_signup_response_message(self, test_client, reset_activities):
        """
        Test that delete signup returns appropriate success message.
        
        AAA Pattern:
        - Arrange: Student in activity
        - Act: Unregister student
        - Assert: Response message contains email and activity name
        """
        # Arrange
        email = "daniel@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"
        
        # Act
        response = test_client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert email in result["message"]
        assert activity_name in result["message"]
