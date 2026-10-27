import unittest
from services.geocoding_service import geocoder
from services.advisory_engine import advisory_engine

class TestAdvisoryEngine(unittest.TestCase):
    def setUp(self):
        self.chn_loc = geocoder.geocode("Chengannur")

    def test_day_vs_night_advisory(self):
        day_res = advisory_engine.calculate_advisory(self.chn_loc, "2026-10-28", "11:00")
        night_res = advisory_engine.calculate_advisory(self.chn_loc, "2026-10-28", "23:30")

        # Day should have higher comfort score than late night
        self.assertGreater(day_res["advisory"]["score"], night_res["advisory"]["score"])
        self.assertIn(day_res["advisory"]["category"], ["Favorable Conditions", "Moderate Comfort"])
        self.assertTrue(night_res["travel_schedule"]["is_night"])
        self.assertFalse(day_res["travel_schedule"]["is_night"])

    def test_score_bounds(self):
        res = advisory_engine.calculate_advisory(self.chn_loc, "2026-10-28", "14:00")
        score = res["advisory"]["score"]
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 100.0)

    def test_nearest_police_station_included(self):
        res = advisory_engine.calculate_advisory(self.chn_loc, "2026-10-28", "14:00")
        self.assertIsNotNone(res["nearest_police_station"])
        self.assertIn("Chengannur", res["nearest_police_station"]["name"])
        self.assertIn("distance_km", res["nearest_police_station"])
        self.assertIn("phone", res["nearest_police_station"])

    def test_contributing_factors_exist(self):
        res = advisory_engine.calculate_advisory(self.chn_loc, "2026-10-28", "14:00")
        factors = res["advisory"]["contributing_factors"]
        self.assertEqual(len(factors), 4)

if __name__ == "__main__":
    unittest.main()
