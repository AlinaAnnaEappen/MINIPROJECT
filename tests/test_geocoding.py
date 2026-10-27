import unittest
from services.geocoding_service import geocoder

class TestGeocodingService(unittest.TestCase):
    def test_local_gazetteer_chengannur(self):
        res = geocoder.geocode("Chengannur")
        self.assertTrue(res["found"])
        self.assertEqual(res["district_id"], "alappuzha")
        self.assertAlmostEqual(res["lat"], 9.3176, places=2)
        self.assertAlmostEqual(res["lon"], 76.6112, places=2)
        self.assertTrue(res["is_local"])

    def test_local_gazetteer_kochi(self):
        res = geocoder.geocode("Kochi")
        self.assertTrue(res["found"])
        self.assertEqual(res["district_id"], "ernakulam")
        self.assertTrue(res["is_local"])

    def test_college_of_engineering_chengannur(self):
        res = geocoder.geocode("College of Engineering Chengannur")
        self.assertTrue(res["found"])
        self.assertEqual(res["district_id"], "alappuzha")

    def test_empty_query(self):
        res = geocoder.geocode("")
        self.assertFalse(res["found"])
        self.assertIn("error", res)

    def test_unknown_location(self):
        res = geocoder.geocode("NonExistentPlaceXYZ987")
        self.assertFalse(res["found"])

if __name__ == "__main__":
    unittest.main()
