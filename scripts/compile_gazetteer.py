import json

gazetteer = [
    # Alappuzha & Chengannur Region
    {"name": "Chengannur", "district": "Alappuzha", "lat": 9.3176, "lon": 76.6112, "category": "Town"},
    {"name": "College of Engineering Chengannur", "district": "Alappuzha", "lat": 9.3168, "lon": 76.6186, "category": "Educational Institution"},
    {"name": "Chengannur Railway Station", "district": "Alappuzha", "lat": 9.3185, "lon": 76.6135, "category": "Transit Hub"},
    {"name": "Chengannur KSRTC Bus Stand", "district": "Alappuzha", "lat": 9.3150, "lon": 76.6140, "category": "Transit Hub"},
    {"name": "Alappuzha", "district": "Alappuzha", "lat": 9.4981, "lon": 76.3388, "category": "District HQ"},
    {"name": "Alappuzha Beach", "district": "Alappuzha", "lat": 9.4925, "lon": 76.3180, "category": "Tourist Location"},
    {"name": "Alappuzha KSRTC Bus Station", "district": "Alappuzha", "lat": 9.4930, "lon": 76.3350, "category": "Transit Hub"},
    {"name": "Mavelikkara", "district": "Alappuzha", "lat": 9.2667, "lon": 76.5500, "category": "Town"},
    {"name": "Kayamkulam", "district": "Alappuzha", "lat": 9.1725, "lon": 76.4998, "category": "Town"},
    {"name": "Cherthala", "district": "Alappuzha", "lat": 9.6843, "lon": 76.3364, "category": "Town"},
    {"name": "Haripad", "district": "Alappuzha", "lat": 9.2842, "lon": 76.4633, "category": "Town"},
    {"name": "Ambalapuzha", "district": "Alappuzha", "lat": 9.3789, "lon": 76.3615, "category": "Town"},

    # Pathanamthitta
    {"name": "Pathanamthitta", "district": "Pathanamthitta", "lat": 9.2648, "lon": 76.7870, "category": "District HQ"},
    {"name": "Adoor", "district": "Pathanamthitta", "lat": 9.1550, "lon": 76.7320, "category": "Town"},
    {"name": "Thiruvalla", "district": "Pathanamthitta", "lat": 9.3835, "lon": 76.5740, "category": "Town"},
    {"name": "Thiruvalla Railway Station", "district": "Pathanamthitta", "lat": 9.3850, "lon": 76.5780, "category": "Transit Hub"},
    {"name": "Pandalam", "district": "Pathanamthitta", "lat": 9.2312, "lon": 76.6841, "category": "Town"},
    {"name": "Aranmula", "district": "Pathanamthitta", "lat": 9.3082, "lon": 76.6853, "category": "Heritage Town"},
    {"name": "Kozhencherry", "district": "Pathanamthitta", "lat": 9.3360, "lon": 76.7080, "category": "Town"},

    # Ernakulam / Kochi
    {"name": "Kochi", "district": "Ernakulam", "lat": 9.9312, "lon": 76.2673, "category": "Major City"},
    {"name": "Ernakulam", "district": "Ernakulam", "lat": 9.9816, "lon": 76.2999, "category": "District HQ"},
    {"name": "MG Road Kochi", "district": "Ernakulam", "lat": 9.9720, "lon": 76.2840, "category": "Commercial Hub"},
    {"name": "Marine Drive Kochi", "district": "Ernakulam", "lat": 9.9790, "lon": 76.2760, "category": "Public Promenade"},
    {"name": "Edappally", "district": "Ernakulam", "lat": 10.0236, "lon": 76.3116, "category": "Transit & Retail Hub"},
    {"name": "Lulu Mall Kochi", "district": "Ernakulam", "lat": 10.0270, "lon": 76.3080, "category": "Commercial Hub"},
    {"name": "Infopark Kakkanad", "district": "Ernakulam", "lat": 10.0120, "lon": 76.3620, "category": "Tech Corridor"},
    {"name": "Vyttila Mobility Hub", "district": "Ernakulam", "lat": 9.9675, "lon": 76.3210, "category": "Transit Hub"},
    {"name": "Fort Kochi", "district": "Ernakulam", "lat": 9.9658, "lon": 76.2428, "category": "Tourist Zone"},
    {"name": "Aluva", "district": "Ernakulam", "lat": 10.1076, "lon": 76.3516, "category": "Transit Hub"},

    # Thiruvananthapuram
    {"name": "Thiruvananthapuram", "district": "Thiruvananthapuram", "lat": 8.5241, "lon": 76.9366, "category": "State Capital"},
    {"name": "Thampanoor", "district": "Thiruvananthapuram", "lat": 8.4870, "lon": 76.9525, "category": "Transit Hub"},
    {"name": "East Fort", "district": "Thiruvananthapuram", "lat": 8.4840, "lon": 76.9450, "category": "Transit & Heritage"},
    {"name": "Kazhakkoottam", "district": "Thiruvananthapuram", "lat": 8.5685, "lon": 76.8710, "category": "Town"},
    {"name": "Technopark Trivandrum", "district": "Thiruvananthapuram", "lat": 8.5580, "lon": 76.8810, "category": "Tech Corridor"},
    {"name": "Kovalam Beach", "district": "Thiruvananthapuram", "lat": 8.4000, "lon": 76.9780, "category": "Tourist Location"},

    # Kottayam
    {"name": "Kottayam", "district": "Kottayam", "lat": 9.5916, "lon": 76.5222, "category": "District HQ"},
    {"name": "Changanassery", "district": "Kottayam", "lat": 9.4445, "lon": 76.5410, "category": "Town"},
    {"name": "Pala", "district": "Kottayam", "lat": 9.7110, "lon": 76.6830, "category": "Town"},
    {"name": "Ettumanoor", "district": "Kottayam", "lat": 9.6670, "lon": 76.5620, "category": "Town"},

    # Kollam
    {"name": "Kollam", "district": "Kollam", "lat": 8.8932, "lon": 76.6141, "category": "District HQ"},
    {"name": "Karunagappally", "district": "Kollam", "lat": 9.0540, "lon": 76.5360, "category": "Town"},
    {"name": "Kottarakkara", "district": "Kollam", "lat": 8.9980, "lon": 76.7720, "category": "Town"},

    # Thrissur
    {"name": "Thrissur", "district": "Thrissur", "lat": 10.5276, "lon": 76.2144, "category": "District HQ"},
    {"name": "Swaraj Round Thrissur", "district": "Thrissur", "lat": 10.5240, "lon": 76.2140, "category": "Commercial Hub"},
    {"name": "Guruvayur", "district": "Thrissur", "lat": 10.5950, "lon": 76.0410, "category": "Pilgrim Center"},
    {"name": "Chalakudy", "district": "Thrissur", "lat": 10.3070, "lon": 76.3330, "category": "Town"},

    # Kozhikode
    {"name": "Kozhikode", "district": "Kozhikode", "lat": 11.2588, "lon": 75.7804, "category": "District HQ"},
    {"name": "SM Street Kozhikode", "district": "Kozhikode", "lat": 11.2530, "lon": 75.7790, "category": "Commercial Hub"},
    {"name": "Kozhikode Beach", "district": "Kozhikode", "lat": 11.2610, "lon": 75.7680, "category": "Public Promenade"},

    # Palakkad
    {"name": "Palakkad", "district": "Palakkad", "lat": 10.7867, "lon": 76.6548, "category": "District HQ"},
    {"name": "Ottapalam", "district": "Palakkad", "lat": 10.7720, "lon": 76.3810, "category": "Town"},

    # Malappuram
    {"name": "Malappuram", "district": "Malappuram", "lat": 11.0510, "lon": 76.0711, "category": "District HQ"},
    {"name": "Manjeri", "district": "Malappuram", "lat": 11.1210, "lon": 76.1215, "category": "Town"},
    {"name": "Perinthalmanna", "district": "Malappuram", "lat": 10.9760, "lon": 76.2260, "category": "Town"},

    # Kannur
    {"name": "Kannur", "district": "Kannur", "lat": 11.8745, "lon": 75.3704, "category": "District HQ"},
    {"name": "Thalassery", "district": "Kannur", "lat": 11.7505, "lon": 75.4920, "category": "Town"},
    {"name": "Payyanur", "district": "Kannur", "lat": 12.1000, "lon": 75.2000, "category": "Town"},

    # Wayanad
    {"name": "Kalpetta", "district": "Wayanad", "lat": 11.6095, "lon": 76.0825, "category": "District HQ"},
    {"name": "Sultan Bathery", "district": "Wayanad", "lat": 11.6640, "lon": 76.2570, "category": "Town"},
    {"name": "Mananthavady", "district": "Wayanad", "lat": 11.8020, "lon": 76.0040, "category": "Town"},

    # Idukki
    {"name": "Munnar", "district": "Idukki", "lat": 10.0889, "lon": 77.0595, "category": "Hill Station"},
    {"name": "Thodupuzha", "district": "Idukki", "lat": 9.8970, "lon": 76.7150, "category": "Town"},
    {"name": "Kattappana", "district": "Idukki", "lat": 9.7520, "lon": 77.1180, "category": "Town"},

    # Kasaragod
    {"name": "Kasaragod", "district": "Kasaragod", "lat": 12.5102, "lon": 74.9852, "category": "District HQ"},
    {"name": "Kanhangad", "district": "Kasaragod", "lat": 12.3120, "lon": 75.0920, "category": "Town"}
]

with open("data/gazetteer_kerala.json", "w", encoding="utf-8") as f:
    json.dump(gazetteer, f, indent=2)

print(f"Saved {len(gazetteer)} gazetteer entries to data/gazetteer_kerala.json")
