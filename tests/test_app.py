import unittest
import json
import os
from app import app
from services.feedback_service import feedback_service

class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_landing_page_branding_and_content(self):
        """Verify simplified branding and removal of academic pills."""
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'SHE SHIELD', res.data)
        self.assertIn(b'Travel with', res.data)
        self.assertIn(b'greater awareness', res.data)
        self.assertIn(b'Plan Your Journey', res.data)
        # Verify academic branding removed from user-facing landing page
        self.assertNotIn(b'College of Engineering Chengannur', res.data)
        self.assertNotIn(b'Academic Advisory', res.data)
        self.assertNotIn(b'Academic Mini Project 2026', res.data)

    def test_plan_page(self):
        """Verify journey planner layout and map integration."""
        res = self.client.get('/plan')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Plan Your Journey', res.data)
        self.assertIn(b'advisory-map', res.data)
        self.assertIn(b'location-input', res.data)

    def test_share_experience_page(self):
        """Verify Share Your Experience page loads with required form fields."""
        res = self.client.get('/share-experience')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Share Your Travel Experience', res.data)
        self.assertIn(b'feedback-form', res.data)
        self.assertIn(b'feedback-location', res.data)
        self.assertIn(b'time_category', res.data)
        self.assertIn(b'comfort_level', res.data)
        self.assertIn(b'factors', res.data)

    def test_feedback_api_valid_submission(self):
        """Verify submitting valid feedback returns 201 and persists."""
        payload = {
            "location": "Aluva Metro Station",
            "time_category": "Evening",
            "comfort_level": "Mostly comfortable",
            "factors": ["Street lighting", "Crowd levels", "Public transport availability"],
            "comments": "Active passenger presence around feeder buses.",
            "would_revisit": "Yes"
        }
        res = self.client.post('/api/feedback', json=payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("message", data["result"])

    def test_feedback_api_invalid_submission(self):
        """Verify submitting invalid feedback returns 400 error."""
        # Missing location
        res = self.client.post('/api/feedback', json={"time_category": "Evening", "comfort_level": "Comfortable"})
        self.assertEqual(res.status_code, 400)
        self.assertFalse(res.get_json()["success"])

        # Invalid time category
        res = self.client.post('/api/feedback', json={"location": "Kochi", "time_category": "Midnight", "comfort_level": "Comfortable"})
        self.assertEqual(res.status_code, 400)

        # Invalid comfort level
        res = self.client.post('/api/feedback', json={"location": "Kochi", "time_category": "Evening", "comfort_level": "Awesome"})
        self.assertEqual(res.status_code, 400)

    def test_feedback_persistence(self):
        """Verify saved feedback records persist in SQLite."""
        test_loc = "Test Persistence Location Thrissur"
        payload = {
            "location": test_loc,
            "time_category": "Morning",
            "comfort_level": "Comfortable",
            "factors": ["Street lighting"],
            "comments": "Testing database persistence.",
            "would_revisit": "Yes"
        }
        res = self.client.post('/api/feedback', json=payload)
        self.assertEqual(res.status_code, 201)

        records = feedback_service.get_records(limit=20)
        matching = [r for r in records if r["location"] == test_loc]
        self.assertTrue(len(matching) > 0)
        self.assertEqual(matching[0]["comfort_level"], "Comfortable")

    def test_admin_feedback_endpoint(self):
        """Verify private developer inspection endpoint."""
        res = self.client.get('/api/admin/feedback?token=she_shield_dev_2026')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("records", data)
        self.assertIn("stats", data)

    def test_api_predict_valid(self):
        """Verify live advisory prediction endpoint generates accurate results."""
        payload = {
            "location": "College of Engineering Chengannur",
            "date": "2026-10-28",
            "time": "21:30"
        }
        res = self.client.post('/api/predict', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data.get("success"))
        result = data["result"]
        self.assertIn("advisory", result)
        self.assertIn("score", result["advisory"])
        self.assertIn("nearest_police_station", result)
        self.assertIn("crime_context", result)
        self.assertEqual(result["location"]["district_name"], "Alappuzha")

    def test_api_health(self):
        """Verify health check returns healthy status."""
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")

if __name__ == '__main__':
    unittest.main()
