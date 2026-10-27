import json
import math
import os
import requests

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
GAZETTEER_PATH = os.path.join(DATA_DIR, "gazetteer_kerala.json")
DISTRICTS_PATH = os.path.join(DATA_DIR, "kerala_districts_crime.json")

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

class GeocodingService:
    def __init__(self):
        self.gazetteer = []
        self.districts = []
        self._load_local_data()

    def _load_local_data(self):
        if os.path.exists(GAZETTEER_PATH):
            with open(GAZETTEER_PATH, "r", encoding="utf-8") as f:
                self.gazetteer = json.load(f)
        if os.path.exists(DISTRICTS_PATH):
            with open(DISTRICTS_PATH, "r", encoding="utf-8") as f:
                dist_data = json.load(f)
                self.districts = dist_data.get("districts", [])

    def map_to_district(self, lat, lon, text_hint=""):
        # 1. Check if text_hint directly matches a district name
        hint_lower = text_hint.lower()
        for d in self.districts:
            if d["name"].lower() in hint_lower or d["id"] in hint_lower:
                return d["id"], d["name"]

        # 2. Otherwise map by minimum Haversine distance to district headquarters/center
        min_dist = float("inf")
        closest_district = None
        for d in self.districts:
            dist = haversine_km(lat, lon, d["center"]["lat"], d["center"]["lon"])
            if dist < min_dist:
                min_dist = dist
                closest_district = d

        if closest_district:
            return closest_district["id"], closest_district["name"]
        return "alappuzha", "Alappuzha"

    def geocode(self, query):
        clean_query = query.strip()
        if not clean_query:
            return {"found": False, "error": "Location query cannot be empty"}

        query_lower = clean_query.lower()

        # Step 1: Local Gazetteer Match (Instant, reliable, offline-ready)
        # Check exact name match first
        for item in self.gazetteer:
            if item["name"].lower() == query_lower:
                dist_id, dist_name = self.map_to_district(item["lat"], item["lon"], item["district"])
                return {
                    "found": True,
                    "name": item["name"],
                    "display_name": f"{item['name']}, {item['district']}, Kerala",
                    "lat": item["lat"],
                    "lon": item["lon"],
                    "district_id": dist_id,
                    "district_name": dist_name,
                    "source": "Verified Local Gazetteer",
                    "is_local": True
                }

        # Check partial/substring match in gazetteer
        for item in self.gazetteer:
            if query_lower in item["name"].lower() or item["name"].lower() in query_lower:
                dist_id, dist_name = self.map_to_district(item["lat"], item["lon"], item["district"])
                return {
                    "found": True,
                    "name": item["name"],
                    "display_name": f"{item['name']}, {item['district']}, Kerala",
                    "lat": item["lat"],
                    "lon": item["lon"],
                    "district_id": dist_id,
                    "district_name": dist_name,
                    "source": "Verified Local Gazetteer",
                    "is_local": True
                }

        # Step 2: Online Nominatim (OpenStreetMap) with Kerala bounding context
        try:
            headers = {"User-Agent": "SheShieldAcademicProject/1.0 (contact: alina.cec.ac.in)"}
            search_text = clean_query if "kerala" in query_lower else f"{clean_query}, Kerala, India"
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                "q": search_text,
                "format": "json",
                "limit": 1,
                "viewbox": "74.8,12.9,77.5,8.1",
                "bounded": 1
            }
            res = requests.get(url, params=params, headers=headers, timeout=4)
            if res.status_code == 200:
                results = res.json()
                if results:
                    top = results[0]
                    lat = float(top["lat"])
                    lon = float(top["lon"])
                    display = top.get("display_name", clean_query)
                    dist_id, dist_name = self.map_to_district(lat, lon, display)
                    return {
                        "found": True,
                        "name": clean_query.title(),
                        "display_name": display,
                        "lat": lat,
                        "lon": lon,
                        "district_id": dist_id,
                        "district_name": dist_name,
                        "source": "OpenStreetMap Nominatim",
                        "is_local": False
                    }
        except Exception:
            pass

        # Step 3: Online Photon (Komoot OSM Geocoder Fallback)
        try:
            photon_url = "https://photon.komoot.io/api/"
            params = {"q": f"{clean_query}, Kerala", "limit": 1}
            headers = {"User-Agent": "SheShieldAcademicProject/1.0"}
            res = requests.get(photon_url, params=params, headers=headers, timeout=4)
            if res.status_code == 200:
                data = res.json()
                features = data.get("features", [])
                if features:
                    feat = features[0]
                    coords = feat["geometry"]["coordinates"]
                    lon, lat = coords[0], coords[1]
                    props = feat.get("properties", {})
                    name = props.get("name", clean_query.title())
                    district_hint = props.get("district") or props.get("county") or ""
                    dist_id, dist_name = self.map_to_district(lat, lon, district_hint)
                    return {
                        "found": True,
                        "name": name,
                        "display_name": f"{name}, {district_hint}, Kerala",
                        "lat": lat,
                        "lon": lon,
                        "district_id": dist_id,
                        "district_name": dist_name,
                        "source": "Photon Geocoder (OSM)",
                        "is_local": False
                    }
        except Exception:
            pass

        return {
            "found": False,
            "error": f"Location '{clean_query}' could not be resolved within Kerala. Please select a known destination or town."
        }

geocoder = GeocodingService()
