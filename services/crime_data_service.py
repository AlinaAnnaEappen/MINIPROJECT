import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CRIME_PATH = os.path.join(DATA_DIR, "kerala_districts_crime.json")

class CrimeDataService:
    def __init__(self):
        self.data = {}
        self.districts_by_id = {}
        self.districts_by_name = {}
        self._load_data()

    def _load_data(self):
        if os.path.exists(CRIME_PATH):
            with open(CRIME_PATH, "r", encoding="utf-8") as f:
                self.data = json.load(f)
                for d in self.data.get("districts", []):
                    self.districts_by_id[d["id"]] = d
                    self.districts_by_name[d["name"].lower()] = d

    def get_all_districts(self):
        return self.data.get("districts", [])

    def get_district_crime(self, district_id_or_name):
        if not district_id_or_name:
            return None
        key = str(district_id_or_name).strip().lower()
        if key in self.districts_by_id:
            return self.districts_by_id[key]
        if key in self.districts_by_name:
            return self.districts_by_name[key]
        # Partial match
        for d_id, d_data in self.districts_by_id.items():
            if d_id in key or key in d_id or d_data["name"].lower() in key:
                return d_data
        # Fallback to Alappuzha if unknown
        return self.districts_by_id.get("alappuzha")

    def get_sources_and_provenance(self):
        return {
            "sources": self.data.get("sources", []),
            "state_totals": self.data.get("state_totals", {}),
            "geographic_level": "District-Level Aggregate Statistics",
            "critical_notice": (
                "Official crime data in India and Kerala is published at the State and District levels. "
                "Precise street-level crime records are not published for public access. "
                "Aggregated district statistics indicate broad regional patterns and should not be misinterpreted "
                "as local micro-incident frequency at specific road coordinates."
            )
        }

crime_service = CrimeDataService()
