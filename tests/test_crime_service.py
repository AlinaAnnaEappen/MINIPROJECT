import unittest
from services.crime_data_service import crime_service

class TestCrimeDataService(unittest.TestCase):
    def test_all_14_districts_present(self):
        districts = crime_service.get_all_districts()
        self.assertEqual(len(districts), 14)
        
        expected_districts = {
            "thiruvananthapuram", "kollam", "pathanamthitta", "alappuzha",
            "kottayam", "idukki", "ernakulam", "thrissur", "palakkad",
            "malappuram", "kozhikode", "wayanad", "kannur", "kasaragod"
        }
        loaded_ids = {d["id"] for d in districts}
        self.assertEqual(expected_districts, loaded_ids)

    def test_district_alappuzha_stats(self):
        d = crime_service.get_district_crime("alappuzha")
        self.assertIsNotNone(d)
        self.assertEqual(d["name"], "Alappuzha")
        self.assertGreater(d["latest_annual_total"], 1000)
        self.assertGreater(d["rate_per_lakh_females"], 50.0)
        self.assertIn("molestation", d["crime_data"]["2024"])
        self.assertIn("rape", d["crime_data"]["2024"])

    def test_district_lookup_case_insensitivity(self):
        d1 = crime_service.get_district_crime("Kozhikode")
        d2 = crime_service.get_district_crime("kozhikode")
        self.assertEqual(d1["id"], d2["id"])

    def test_sources_and_provenance(self):
        prov = crime_service.get_sources_and_provenance()
        self.assertIn("sources", prov)
        self.assertIn("Kerala Police Crime Statistics Portal (SCRB)", str(prov["sources"]))
        self.assertEqual(prov["geographic_level"], "District-Level Aggregate Statistics")

if __name__ == "__main__":
    unittest.main()
