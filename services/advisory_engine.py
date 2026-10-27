import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from services.crime_data_service import crime_service
from services.osm_service import osm_service

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
GB_REG_PATH = os.path.join(MODEL_DIR, "transit_safety_regressor.pkl")
GB_CLF_PATH = os.path.join(MODEL_DIR, "transit_safety_model.pkl")

class AdvisoryEngine:
    def __init__(self):
        self.reg_model = None
        self.clf_model = None
        self._load_models()

    def _load_models(self):
        try:
            if os.path.exists(GB_REG_PATH):
                self.reg_model = joblib.load(GB_REG_PATH)
            if os.path.exists(GB_CLF_PATH):
                self.clf_model = joblib.load(GB_CLF_PATH)
        except Exception as e:
            print("Notice: ML models loading fallback:", e)

    def calculate_advisory(self, location_data, travel_date_str, travel_time_str):
        """
        Computes a multi-layered, grounded Safety & Comfort Index (0-100%) and advisory message.
        """
        lat = location_data["lat"]
        lon = location_data["lon"]
        district_id = location_data["district_id"]
        location_name = location_data["name"]

        # 1. Parse Temporal Features
        travel_hour = 12
        is_night = 0
        is_weekend = 0
        formatted_time = "12:00 PM"
        formatted_date = travel_date_str

        try:
            # Parse time (handles "14:30", "2:30 PM", "9 AM", etc.)
            t_str = travel_time_str.strip().upper()
            if "AM" in t_str or "PM" in t_str:
                parsed_t = datetime.strptime(t_str, "%I:%M %p" if ":" in t_str else "%I %p")
            else:
                parsed_t = datetime.strptime(t_str, "%H:%M")
            travel_hour = parsed_t.hour
            formatted_time = parsed_t.strftime("%I:%M %p")
        except Exception:
            travel_hour = 14
            formatted_time = travel_time_str

        try:
            parsed_d = datetime.strptime(travel_date_str, "%Y-%m-%d")
            formatted_date = parsed_d.strftime("%A, %B %d, %Y")
            if parsed_d.weekday() >= 5:
                is_weekend = 1
        except Exception:
            pass

        # Night definition: 19:00 to 06:00
        if travel_hour >= 19 or travel_hour <= 5:
            is_night = 1

        # 2. Component 1: Regional Crime Context Score (0-100)
        # Based on verified Kerala Police SCRB / NCRB statistics
        district_info = crime_service.get_district_crime(district_id)
        if district_info:
            pub_crime_rate = district_info.get("public_space_crime_rate", 28.5)
            # In Kerala, public space crime rate per lakh females ranges from 24.9 (Idukki) to 36.1 (Ernakulam).
            # We map this smoothly: baseline 100 minus normalized crime pressure
            crime_score = max(50.0, min(95.0, 100.0 - (pub_crime_rate * 1.05)))
            district_name = district_info["name"]
            crime_stats_summary = {
                "district": district_name,
                "latest_annual_crimes": district_info["latest_annual_total"],
                "rate_per_lakh_females": district_info["rate_per_lakh_females"],
                "public_space_crime_rate": pub_crime_rate,
                "domestic_crime_rate": district_info.get("domestic_crime_rate", 25.0),
                "relative_risk_category": district_info["relative_risk_category"],
                "police_helpline": district_info.get("helpline", {})
            }
        else:
            crime_score = 75.0
            crime_stats_summary = None

        # 3. Component 2: Temporal & Environmental Factor (0-100)
        if 6 <= travel_hour < 18:
            # Daytime
            temporal_score = 92.0
            time_context = "Daylight Hours (Optimal Visibility & Commercial Activity)"
        elif 18 <= travel_hour < 21:
            # Dusk / Early Evening
            temporal_score = 78.0
            time_context = "Early Evening (Active Public Transit & Moderate Visibility)"
        elif 21 <= travel_hour < 24:
            # Late Night
            temporal_score = 58.0
            time_context = "Late Night (Reduced Footfall, Decreased Public Transit Frequency)"
        else:
            # Midnight / Predawn (00:00 - 05:59)
            temporal_score = 48.0
            time_context = "Predawn / Midnight (Minimal Pedestrian Activity, Lower Natural Surveillance)"

        if is_weekend:
            # Slight adjustment for altered weekend transport schedules
            temporal_score -= 2.0

        # 4. Component 3: Emergency & Police Station Proximity (0-100)
        nearby_stations = osm_service.get_nearby_police_stations(lat, lon, limit=5)
        nearest_station = nearby_stations[0] if nearby_stations else None
        nearest_ps_dist = nearest_station["distance_km"] if nearest_station else 15.0

        if nearest_ps_dist <= 2.0:
            infra_score = 95.0
            ps_desc = f"Immediate proximity ({nearest_ps_dist} km to {nearest_station['name']})"
        elif nearest_ps_dist <= 5.0:
            infra_score = 82.0
            ps_desc = f"Moderate distance ({nearest_ps_dist} km to {nearest_station['name']})"
        elif nearest_ps_dist <= 10.0:
            infra_score = 68.0
            ps_desc = f"Standard distance ({nearest_ps_dist} km to {nearest_station['name']})"
        else:
            infra_score = 52.0
            ps_desc = f"Extended response distance ({nearest_ps_dist} km to {nearest_station['name']})"

        # Bonus if nearest station is a Women Police Station or has Pink Patrol
        has_women_station_nearby = any(s.get("is_women_cell") for s in nearby_stations[:3])
        if has_women_station_nearby:
            infra_score = min(100.0, infra_score + 4.0)

        # 5. Component 4: Machine Learning Inference (Transit Perception Model)
        # Using empirical feature input: [cctv, female_staff, lighting, emergency_buttons, reserved_seats, announcements, driver_verified, crowd_high, is_night]
        # In a generic destination query, we evaluate conservative expected conditions:
        ml_score = 70.0
        ml_category = "Moderate"
        if self.reg_model is not None:
            try:
                # Create DataFrame with exact column names to match model training
                feature_names = [
                    'cctv', 'female_staff', 'lighting', 'emergency_buttons',
                    'reserved_seats', 'announcements', 'driver_verified',
                    'crowd_high', 'is_night'
                ]
                sample_df = pd.DataFrame([[0, 0, lighting_expected, 0, 1, 0, 0, crowd_expected, is_night]], columns=feature_names)
                ml_score = float(self.reg_model.predict(sample_df)[0])
                ml_score = max(35.0, min(95.0, ml_score))
            except Exception:
                ml_score = 70.0

        # 6. Multi-Factor Synthesis (Composite Comfort & Safety Index)
        # Weights: 35% Crime Data, 30% Temporal Factor, 20% Emergency Proximity, 15% ML Model
        composite_score = round(
            (0.35 * crime_score) +
            (0.30 * temporal_score) +
            (0.20 * infra_score) +
            (0.15 * ml_score),
            1
        )
        composite_score = max(15.0, min(98.0, composite_score))

        # 7. Category & Actionable Advisory Generation
        if composite_score >= 75.0:
            category = "Favorable Conditions"
            badge_color = "safe"  # Green
            advisory_text = (
                f"Conditions for travelling to {location_name} are assessed as generally favorable. "
                "Daylight hours, active commercial presence, and accessible emergency response infrastructure "
                "support a confident travel experience."
            )
            recommendations = [
                "Proceed with normal journey plans.",
                "Use established public transport and official ride-hailing services.",
                "Maintain general personal awareness as in any public destination."
            ]
        elif composite_score >= 50.0:
            category = "Moderate Comfort"
            badge_color = "cautious"  # Yellow
            advisory_text = (
                f"Moderate comfort level identified for {location_name} during the selected time. "
                "While general public order is maintained, environmental factors such as evening hours or moderate "
                "emergency proximity warrant standard vigilance."
            )
            recommendations = [
                "Prefer main, well-lit arterial roads and verified transit stops.",
                "Keep emergency helpline numbers (112 / 1091) saved on your device.",
                "Share your live journey status with a family member or trusted contact if travelling alone."
            ]
        else:
            category = "Caution Recommended"
            badge_color = "unsafe"  # Red / Caution
            advisory_text = (
                f"Elevated caution is advised for travel to {location_name} at this time. "
                "Late-night hours, reduced street activity, or higher regional crime pressure indicate "
                "the necessity of pre-planned travel arrangements."
            )
            recommendations = [
                "Avoid unlit or isolated shortcuts, desolate alleys, and quiet transit halts.",
                "Pre-book verified transportation (e.g. pre-paid taxi or direct rides) before departing.",
                "Save the nearest police station number and utilize Kerala Police Pink Patrol assistance if needed."
            ]

        # Factors Contributing
        contributing_factors = [
            {"factor": "District Crime Pressure", "score": round(crime_score, 1), "impact": "Positive" if crime_score >= 75 else "Neutral" if crime_score >= 60 else "Adverse", "detail": f"Official SCRB {crime_stats_summary['district'] if crime_stats_summary else ''} rate: {crime_stats_summary['rate_per_lakh_females'] if crime_stats_summary else ''} per lakh females."},
            {"factor": "Time & Lighting", "score": round(temporal_score, 1), "impact": "Positive" if not is_night else "Adverse", "detail": time_context},
            {"factor": "Police & Emergency Access", "score": round(infra_score, 1), "impact": "Positive" if nearest_ps_dist <= 5.0 else "Neutral", "detail": ps_desc},
            {"factor": "Transit Comfort Prediction", "score": round(ml_score, 1), "impact": "Positive" if ml_score >= 70 else "Neutral", "detail": "Machine learning model estimation based on infrastructure and time proxies."}
        ]

        return {
            "location": {
                "name": location_name,
                "display_name": location_data.get("display_name", location_name),
                "lat": lat,
                "lon": lon,
                "district_id": district_id,
                "district_name": district_name if district_info else location_data.get("district_name", "")
            },
            "travel_schedule": {
                "date": formatted_date,
                "time": formatted_time,
                "hour": travel_hour,
                "is_night": bool(is_night),
                "is_weekend": bool(is_weekend)
            },
            "advisory": {
                "score": composite_score,
                "category": category,
                "badge_color": badge_color,
                "summary": advisory_text,
                "recommendations": recommendations,
                "contributing_factors": contributing_factors
            },
            "crime_context": crime_stats_summary,
            "nearby_police_stations": nearby_stations,
            "nearest_police_station": nearest_station,
            "data_provenance": {
                "crime_source": "Kerala Police State Crime Records Bureau (SCRB) & NCRB Crime in India",
                "geographic_level": "District-Level Aggregate Statistics",
                "mapping_source": "OpenStreetMap & Official Police Directory",
                "limitations": "Aggregated statistics describe regional patterns and do not predict instantaneous individual crime events. This system functions as a pre-travel decision aid, not an emergency dispatcher."
            }
        }

advisory_engine = AdvisoryEngine()
