import requests
import socket

def get_all_safety_features(lat, lon):
    # The 'nw' captures both points and buildings
    query = f"""
    [out:json];
    (
      nw["amenity"="police"](around:5000, {lat}, {lon});
      nw["amenity"="hospital"](around:5000, {lat}, {lon});
      nw["highway"="street_lamp"](around:1500, {lat}, {lon});
    );
    out tags;
    """
    
    url = "https://overpass-api.de/api/interpreter"
    
    try:
        # We add a timeout=10 so the code doesn't hang forever if internet is slow
        response = requests.get(url, params={'data': query}, timeout=10)
        response.raise_for_status() # Check if the website actually responded
        
        data = response.json()
        police, hospitals, lights = 0, 0, 0
        
        for element in data.get('elements', []):
            tags = element.get('tags', {})
            if tags.get('amenity') == 'police':
                police += 1
            elif tags.get('amenity') == 'hospital':
                hospitals += 1
            elif tags.get('highway') == 'street_lamp':
                lights += 1
                
        return police, hospitals, lights

    except requests.exceptions.ConnectionError:
        print("❌ Error: No internet connection or Map Server is down.")
        return 0, 0, 0
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
        return 0, 0, 0

# --- TESTING ---
my_lat =9.9679032 
my_lon =76.2444378
p, h, l = get_all_safety_features(my_lat, my_lon)

print(f"\n---  SAFETY DATA ---")
print(f"Police Stations: {p}")
print(f"Hospitals: {h}")
print(f"Street Lights: {l}")