"""
Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern.
"""

import pytest


class TestSignup:
    """Test suite for activity signup functionality."""

    def test_signup_student_successfully(self, test_client, reset_activities):
        """
        Test that a student can successfully sign up for an activity.
        
        AAA Pattern:
        - Arrange: Prepare email and activity name
        - Act: Send POST request to signup endpoint
        - Assert: Response indicates success and status is 200
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity_name = "Chess Club"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "message" in result
        assert email in result["message"]
        assert activity_name in result["message"]

    def test_signup_adds_participant_to_activity(self, test_client, reset_activities):
        """
        Test that signup actually adds the participant to the activity's participant list.
        
        AAA Pattern:
        - Arrange: Get initial participants count
        - Act: Sign up a new student
        - Assert: Verify participant was added
        """
        # Arrange
        email = "newstudent@mergington.edu"
        activity_name = "Programming Class"
        initial_response = test_client.get("/activities")
        initial_count = len(initial_response.json()[activity_name]["participants"])
        
        # Act
        test_client.post(f"/activities/{activity_name}/signup?email={email}")
        
        # Assert
        updated_response = test_client.get("/activities")
        updated_participants = updated_response.json()[activity_name]["participants"]
        assert len(updated_participants) == initial_count + 1
        assert email in updated_participants

    def test_signup_nonexistent_activity_returns_404(self, test_client, reset_activities):
        """
        Test that signing up for a non-existent activity returns 404 error.
        
        AAA Pattern:
        - Arrange: Prepare request with invalid activity name
        - Act: Send POST request to signup
        - Assert: Response is 404 with appropriate error message
        """
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = test_client.post(
            f"/activities/{nonexistent_activity}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "not found" in result["detail"].lower()

    def test_signup_duplicate_registration_returns_400(self, test_client, reset_activities):
        """
        Test that a student cannot register twice for the same activity.
        
        AAA Pattern:
        - Arrange: Student already exists in activity
        - Act: Attempt to sign up same student again
        - Assert: Response is 400 with duplicate error message
        """
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"
        
        # Act
        response = test_client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "already signed up" in result["detail"].lower()

    def test_signup_prevents_double_registration(self, test_client, reset_activities):
        """
        Test that a student cannot sign up twice in succession.
        
        AAA Pattern:
        - Arrange: Prepare email and activity
        - Act: Sign up first time (success), then attempt to sign up again
        - Assert: First signup succeeds, second signup fails with 400
        """
        # Arrange
        email = "unique@mergington.edu"
        activity_name = "Art Club"
        
        # Act - First signup
        first_response = test_client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Act - Second signup (should fail)
        second_response = test_client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert first_response.status_code == 200
        assert second_response.status_code == 400
        assert "already signed up" in second_response.json()["detail"].lower()
