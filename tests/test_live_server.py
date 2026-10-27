import urllib.request
import json

def test_live_server():
    base_url = "http://127.0.0.1:5000"

    # 1. Health Check
    with urllib.request.urlopen(f"{base_url}/api/health") as resp:
        health_data = json.loads(resp.read().decode())
        print(f"[LIVE TEST 1] Health check: {health_data['status']}")
        assert health_data["status"] == "healthy"

    # 2. Landing Page check
    with urllib.request.urlopen(f"{base_url}/") as resp:
        html = resp.read().decode()
        print(f"[LIVE TEST 2] Landing page status: {resp.status}")
        assert resp.status == 200
        assert "SHE SHIELD" in html
        assert "Travel with" in html
        assert "greater awareness" in html
        assert "Plan Your Journey" in html
        assert "College of Engineering Chengannur" not in html

    # 3. Plan Journey Page
    with urllib.request.urlopen(f"{base_url}/plan") as resp:
        html = resp.read().decode()
        print(f"[LIVE TEST 3] Planner page status: {resp.status}")
        assert resp.status == 200
        assert "Plan Your Journey" in html
        assert "advisory-map" in html

    # 4. Journey Advisory Generation (Real backend ML + Crime Data)
    predict_payload = json.dumps({
        "location": "Chengannur",
        "date": "2026-10-28",
        "time": "21:30"
    }).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/api/predict", data=predict_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        pred = json.loads(resp.read().decode())
        print(f"[LIVE TEST 4] Advisory response success: {pred.get('success')}")
        assert pred.get("success") is True
        res = pred["result"]
        print(f"       -> Location: {res['location']['name']} ({res['location']['district_name']})")
        print(f"       -> Score: {res['advisory']['score']}/100 ({res['advisory']['category']})")
        print(f"       -> Nearest Station: {res['nearest_police_station']['name']} ({res['nearest_police_station']['distance_km']} km)")

    # 5. Share Your Experience Page
    with urllib.request.urlopen(f"{base_url}/share-experience") as resp:
        html = resp.read().decode()
        print(f"[LIVE TEST 5] Feedback page status: {resp.status}")
        assert resp.status == 200
        assert "Share Your Travel Experience" in html
        assert "feedback-form" in html

    # 6. Submit User Feedback
    feedback_payload = json.dumps({
        "location": "Aluva Railway Station",
        "time_category": "Evening",
        "comfort_level": "Mostly comfortable",
        "factors": ["Street lighting", "Public transport availability"],
        "comments": "Active bus connections outside main gate.",
        "would_revisit": "Yes"
    }).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/api/feedback", data=feedback_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as resp:
        fb_resp = json.loads(resp.read().decode())
        print(f"[LIVE TEST 6] Feedback submission success: {fb_resp.get('success')}")
        assert resp.status == 201
        assert fb_resp.get("success") is True
        print(f"       -> Server message: {fb_resp['result']['message']}")

    # 7. Private Developer Inspection of Stored Feedback
    with urllib.request.urlopen(f"{base_url}/api/admin/feedback?token=she_shield_dev_2026") as resp:
        admin_data = json.loads(resp.read().decode())
        print(f"[LIVE TEST 7] Developer feedback records count: {len(admin_data['records'])}")
        assert resp.status == 200
        assert admin_data.get("success") is True
        assert len(admin_data["records"]) > 0

    # 8. Test Invalid Feedback Handling
    invalid_payload = json.dumps({
        "location": "",
        "time_category": "Evening",
        "comfort_level": "Comfortable"
    }).encode("utf-8")
    req = urllib.request.Request(f"{base_url}/api/feedback", data=invalid_payload, headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req)
        assert False, "Should have returned 400 for empty location"
    except urllib.error.HTTPError as e:
        print(f"[LIVE TEST 8] Invalid submission rejected with HTTP status: {e.code}")
        assert e.code == 400

    print("\nALL 8 LIVE INTEGRATION TESTS PASSED SUCCESSFULLY ON PORT 5000!")

if __name__ == "__main__":
    test_live_server()
