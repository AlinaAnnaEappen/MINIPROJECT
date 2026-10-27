import os
import json
from datetime import datetime, timezone
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from services.geocoding_service import geocoder
from services.crime_data_service import crime_service
from services.osm_service import osm_service
from services.advisory_engine import advisory_engine
from services.feedback_service import feedback_service

app = Flask(__name__)
CORS(app)

# Ensure templates and static folders are properly configured
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plan')
def plan():
    return render_template('plan.html')

@app.route('/share-experience')
@app.route('/feedback')
def share_experience():
    return render_template('feedback.html')

@app.route('/methodology')
def methodology():
    return render_template('methodology.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# =====================================================================
# REST API Endpoints
# =====================================================================

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """
    Submits user travel experience feedback.
    Saves anonymously to persistent SQLite database for research.
    Does NOT retrain machine learning models.
    """
    data = request.get_json(silent=True) or {}
    success, result = feedback_service.validate_and_save(data)
    if not success:
        return jsonify({"success": False, "error": result}), 400
    return jsonify({"success": True, "result": result}), 201

@app.route('/api/admin/feedback', methods=['GET'])
def admin_feedback():
    """
    Private developer-only inspection endpoint.
    Protected by simple dev token check or local host access.
    """
    token = request.args.get('token', '')
    is_local = request.remote_addr in ['127.0.0.1', '::1', 'localhost']
    if token != 'she_shield_dev_2026' and not is_local:
        return jsonify({"error": "Unauthorized access."}), 403

    limit = min(int(request.args.get('limit', 50)), 200)
    records = feedback_service.get_records(limit=limit)
    stats = feedback_service.get_summary_stats()
    return jsonify({
        "success": True,
        "total_records": len(records),
        "stats": stats,
        "records": records
    })


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "SHE SHIELD – Women Travel Safety and Comfort Index System",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "models_loaded": {
            "gradient_boosting_regressor": advisory_engine.reg_model is not None,
            "gradient_boosting_classifier": advisory_engine.clf_model is not None
        },
        "datasets": {
            "districts_count": len(crime_service.get_all_districts()),
            "mapped_police_stations": len(osm_service.get_all_police_stations()),
            "gazetteer_entries": len(geocoder.gazetteer)
        }
    })

@app.route('/api/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('q', '').strip().lower()
    if not query or len(query) < 2:
        return jsonify({"matches": []})

    matches = []
    for item in geocoder.gazetteer:
        name_lower = item["name"].lower()
        dist_lower = item["district"].lower()
        if query in name_lower or query in dist_lower:
            matches.append({
                "name": item["name"],
                "district": item["district"],
                "lat": item["lat"],
                "lon": item["lon"],
                "category": item.get("category", "Location")
            })
            if len(matches) >= 8:
                break

    return jsonify({"matches": matches})

@app.route('/api/districts', methods=['GET'])
def get_districts():
    return jsonify({
        "total": len(crime_service.get_all_districts()),
        "districts": crime_service.get_all_districts()
    })

@app.route('/api/police-stations', methods=['GET'])
def get_police_stations():
    stations = osm_service.get_all_police_stations()
    district_filter = request.args.get('district', '').strip().lower()
    if district_filter:
        stations = [s for s in stations if s["district"].lower() == district_filter]
    return jsonify({
        "total": len(stations),
        "stations": stations
    })

@app.route('/api/predict', methods=['POST'])
def predict_safety():
    """
    Main Advisory Prediction Endpoint.
    Receives: { location: string, date: YYYY-MM-DD, time: string (e.g. "21:30" or "9 PM") }
    Returns: Complete structured advisory JSON with crime context and mapped stations.
    """
    data = request.get_json(silent=True) or {}
    location_query = data.get('location', '').strip()
    travel_date = data.get('date', '').strip()
    travel_time = data.get('time', '').strip()

    if not location_query:
        return jsonify({"success": False, "error": "Destination location is required."}), 400

    if not travel_date:
        travel_date = datetime.now().strftime("%Y-%m-%d")

    if not travel_time:
        travel_time = datetime.now().strftime("%H:%M")

    # 1. Geocode Destination
    geo_result = geocoder.geocode(location_query)
    if not geo_result or not geo_result.get("found"):
        return jsonify({
            "success": False,
            "error": geo_result.get("error", f"Location '{location_query}' could not be identified in Kerala.")
        }), 404

    # 2. Calculate Grounded Advisory
    try:
        advisory_result = advisory_engine.calculate_advisory(geo_result, travel_date, travel_time)
        return jsonify({
            "success": True,
            "result": advisory_result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Advisory calculation failed: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[SHE SHIELD] Starting Web Server on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=False)

