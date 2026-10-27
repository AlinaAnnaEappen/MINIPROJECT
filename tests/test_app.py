import unittest
import json
from app import app

class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_landing_page(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'SHE SHIELD', res.data)
        self.assertIn(b'Plan Your Journey', res.data)

    def test_plan_page(self):
        res = self.client.get('/plan')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Interactive Advisory Console', res.data)
        self.assertIn(b'advisory-map', res.data)

    def test_methodology_page(self):
        res = self.client.get('/methodology')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Data Sources, Methodology & Evaluation', res.data)
        self.assertIn(b'Kerala Police SCRB', res.data)

    def test_about_page(self):
        res = self.client.get('/about')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'College of Engineering Chengannur', res.data)

    def test_contact_page(self):
        res = self.client.get('/contact')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'112', res.data)
        self.assertIn(b'1091', res.data)

    def test_api_health(self):
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertTrue(data["models_loaded"]["gradient_boosting_regressor"])

    def test_api_autocomplete(self):
        res = self.client.get('/api/autocomplete?q=chen')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(len(data["matches"]) > 0)
        names = [m["name"] for m in data["matches"]]
        self.assertTrue(any("Chengannur" in n for n in names))

    def test_api_predict_valid(self):
        payload = {
            "location": "Chengannur",
            "date": "2026-10-28",
            "time": "14:00"
        }
        res = self.client.post('/api/predict', json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertIn("score", data["result"]["advisory"])
        self.assertIn("nearby_police_stations", data["result"])

    def test_api_predict_missing_location(self):
        res = self.client.post('/api/predict', json={})
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertFalse(data["success"])

if __name__ == "__main__":
    unittest.main()
