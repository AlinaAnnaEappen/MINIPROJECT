import urllib.request
import json

def test_live_server():
    health_url = "http://127.0.0.1:5000/api/health"
    with urllib.request.urlopen(health_url) as response:
        health_data = json.loads(response.read().decode())
        print(f"Health check: {health_data['status']}")
        assert health_data["status"] == "healthy"

    predict_url = "http://127.0.0.1:5000/api/predict"
    payload = json.dumps({
        "location": "College of Engineering Chengannur",
        "date": "2026-10-28",
        "time": "21:30"
    }).encode("utf-8")
    
    req = urllib.request.Request(predict_url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read().decode())
        print(f"Advisory success: {res.get('success')}")
        assert res.get("success") is True
        
        advisory_payload = res["result"]
        adv = advisory_payload["advisory"]
        loc = advisory_payload["location"]
        stn = advisory_payload["nearest_police_station"]
        
        print(f"Location resolved: {loc['name']} ({loc['district_name']})")
        print(f"Coordinates: ({loc['lat']}, {loc['lon']})")
        print(f"Index Score: {adv['score']}/100")
        print(f"Category: {adv['category']}")
        print(f"Nearest Station: {stn['name']} ({stn['distance_km']} km away)")
        print(f"Emergency Phone: {stn['phone']}")
        print(f"Contributing factors count: {len(adv['contributing_factors'])}")
        print("Live server test PASSED successfully!")

if __name__ == "__main__":
    test_live_server()
