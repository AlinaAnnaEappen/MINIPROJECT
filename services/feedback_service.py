import sqlite3
import os
import json
from datetime import datetime, timezone

# Path to persistent SQLite database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "feedback.db")

ALLOWED_TIME_CATEGORIES = [
    "Morning",
    "Afternoon",
    "Evening",
    "Late night"
]

ALLOWED_COMFORT_LEVELS = [
    "Comfortable",
    "Mostly comfortable",
    "Somewhat uncomfortable",
    "Very uncomfortable"
]

ALLOWED_FACTORS = [
    "Street lighting",
    "Crowd levels",
    "Public transport availability",
    "Availability of help",
    "Road and pedestrian conditions",
    "Unwanted attention or harassment",
    "Other"
]

ALLOWED_REVISIT = ["Yes", "No", "Maybe", ""]


class FeedbackService:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Create feedback table if not already existing."""
        conn = self._get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT NOT NULL,
                    time_category TEXT NOT NULL,
                    comfort_level TEXT NOT NULL,
                    factors TEXT NOT NULL,
                    comments TEXT,
                    would_revisit TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def validate_and_save(self, payload):
        """
        Validates submitted feedback payload and stores record persistently.
        Returns: (success: bool, result_or_error: dict/str)
        """
        if not isinstance(payload, dict):
            return False, "Invalid payload format."

        # 1. Location validation
        location = str(payload.get("location", "")).strip()
        if not location:
            return False, "Approximate location is required."
        if len(location) < 2 or len(location) > 120:
            return False, "Location must be between 2 and 120 characters."

        # 2. Time category validation
        time_category = str(payload.get("time_category", "")).strip()
        if time_category not in ALLOWED_TIME_CATEGORIES:
            return False, f"Time category must be one of: {', '.join(ALLOWED_TIME_CATEGORIES)}"

        # 3. Comfort level validation
        comfort_level = str(payload.get("comfort_level", "")).strip()
        if comfort_level not in ALLOWED_COMFORT_LEVELS:
            return False, f"Comfort level must be one of: {', '.join(ALLOWED_COMFORT_LEVELS)}"

        # 4. Factors validation (allow multiple selections)
        raw_factors = payload.get("factors", [])
        if isinstance(raw_factors, str):
            raw_factors = [raw_factors]
        elif not isinstance(raw_factors, list):
            raw_factors = []

        validated_factors = [f for f in raw_factors if f in ALLOWED_FACTORS]

        # 5. Optional comments
        comments = str(payload.get("comments", "")).strip()
        if len(comments) > 1000:
            return False, "Comments cannot exceed 1000 characters."

        # 6. Optional would_revisit
        would_revisit = str(payload.get("would_revisit", "")).strip()
        if would_revisit and would_revisit not in ALLOWED_REVISIT:
            would_revisit = ""

        # Insert record into SQLite
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO user_feedback (
                    location, time_category, comfort_level, factors, comments, would_revisit, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                location,
                time_category,
                comfort_level,
                json.dumps(validated_factors),
                comments,
                would_revisit,
                datetime.now(timezone.utc).isoformat()
            ))
            conn.commit()
            record_id = cursor.lastrowid

            return True, {
                "id": record_id,
                "message": "Thank you for sharing your experience. Your report helps build better community travel insights without compromising personal privacy.",
                "location": location,
                "time_category": time_category,
                "comfort_level": comfort_level
            }
        except Exception as e:
            return False, f"Database error saving feedback: {str(e)}"
        finally:
            conn.close()

    def get_records(self, limit=50):
        """Private developer inspection method to read stored feedback."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, location, time_category, comfort_level, factors, comments, would_revisit, created_at
                FROM user_feedback
                ORDER BY id DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()

            records = []
            for row in rows:
                factors_list = []
                try:
                    factors_list = json.loads(row["factors"])
                except Exception:
                    factors_list = []

                records.append({
                    "id": row["id"],
                    "location": row["location"],
                    "time_category": row["time_category"],
                    "comfort_level": row["comfort_level"],
                    "factors": factors_list,
                    "comments": row["comments"],
                    "would_revisit": row["would_revisit"],
                    "created_at": row["created_at"]
                })
            return records
        except Exception as e:
            print(f"Error fetching feedback records: {e}")
            return []
        finally:
            conn.close()

    def get_summary_stats(self):
        """Returns aggregate totals without exposing individual comments."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as total FROM user_feedback")
            total = cursor.fetchone()["total"]

            cursor.execute("""
                SELECT comfort_level, COUNT(*) as count 
                FROM user_feedback 
                GROUP BY comfort_level
            """)
            by_comfort = {row["comfort_level"]: row["count"] for row in cursor.fetchall()}

            return {
                "total_submissions": total,
                "by_comfort_level": by_comfort
            }
        except Exception:
            return {"total_submissions": 0, "by_comfort_level": {}}
        finally:
            conn.close()



# Global singleton instance
feedback_service = FeedbackService()
