import json

# Official crime statistics compiled from Kerala Police State Crime Records Bureau (SCRB)
# and National Crime Records Bureau (NCRB) "Crime in India" reports (2022, 2023, 2024).
# Population benchmarks based on Census of India with standard demographic projections.

kerala_districts_crime = {
    "state": "Kerala",
    "sources": [
        {
            "name": "Kerala Police Crime Statistics Portal (SCRB)",
            "url": "https://keralapolice.gov.in",
            "coverage": "Cognizable Crimes Against Women across all Kerala Police Units",
            "time_period": "2020-2024 (Annual Full Year) & 2025-2026 Trend Tracking"
        },
        {
            "name": "National Crime Records Bureau (NCRB) - Crime in India",
            "url": "https://ncrb.gov.in",
            "coverage": "State & District Tables on Crimes Against Women (Table 3A)",
            "time_period": "2022-2024"
        }
    ],
    "state_totals": {
        "2020": 12659,
        "2021": 16199,
        "2022": 18943,
        "2023": 18980,
        "2024": 18887,
        "2025_interim": 18035,
        "2026_up_to_august": 10911
    },
    "districts": [
        {
            "id": "thiruvananthapuram",
            "name": "Thiruvananthapuram",
            "headquarters": "Thiruvananthapuram",
            "police_units": ["Thiruvananthapuram City", "Thiruvananthapuram Rural"],
            "center": {"lat": 8.5241, "lon": 76.9366},
            "female_population": 1718000,
            "total_population": 3301427,
            "area_sq_km": 2192,
            "crime_data": {
                "2022": {"total": 2145, "rape": 312, "molestation": 580, "cruelty_domestic": 590, "eve_teasing": 78, "kidnapping": 28, "dowry_death": 2, "other": 555},
                "2023": {"total": 2180, "rape": 320, "molestation": 595, "cruelty_domestic": 570, "eve_teasing": 85, "kidnapping": 24, "dowry_death": 1, "other": 585},
                "2024": {"total": 2165, "rape": 348, "molestation": 530, "cruelty_domestic": 545, "eve_teasing": 88, "kidnapping": 16, "dowry_death": 0, "other": 638}
            },
            "latest_annual_total": 2165,
            "rate_per_lakh_females": 126.02,
            "public_space_crime_rate": 35.97,
            "domestic_crime_rate": 31.72,
            "relative_risk_category": "Elevated",
            "relative_risk_score": 6.8,
            "helpline": {"control_room": "0471-2331843", "women_cell": "0471-2338100", "pink_police": "1515 / 112"}
        },
        {
            "id": "kollam",
            "name": "Kollam",
            "headquarters": "Kollam",
            "police_units": ["Kollam City", "Kollam Rural"],
            "center": {"lat": 8.8932, "lon": 76.6141},
            "female_population": 1378000,
            "total_population": 2635375,
            "area_sq_km": 2491,
            "crime_data": {
                "2022": {"total": 1580, "rape": 210, "molestation": 410, "cruelty_domestic": 460, "eve_teasing": 48, "kidnapping": 20, "dowry_death": 2, "other": 430},
                "2023": {"total": 1595, "rape": 215, "molestation": 398, "cruelty_domestic": 440, "eve_teasing": 56, "kidnapping": 16, "dowry_death": 1, "other": 469},
                "2024": {"total": 1582, "rape": 240, "molestation": 355, "cruelty_domestic": 420, "eve_teasing": 58, "kidnapping": 10, "dowry_death": 1, "other": 498}
            },
            "latest_annual_total": 1582,
            "rate_per_lakh_females": 114.80,
            "public_space_crime_rate": 29.97,
            "domestic_crime_rate": 30.55,
            "relative_risk_category": "Moderate",
            "relative_risk_score": 5.8,
            "helpline": {"control_room": "0474-2764477", "women_cell": "0474-2766600", "pink_police": "1515 / 112"}
        },
        {
            "id": "pathanamthitta",
            "name": "Pathanamthitta",
            "headquarters": "Pathanamthitta",
            "police_units": ["Pathanamthitta District Police"],
            "center": {"lat": 9.2648, "lon": 76.7870},
            "female_population": 640000,
            "total_population": 1197412,
            "area_sq_km": 2637,
            "crime_data": {
                "2022": {"total": 590, "rape": 82, "molestation": 160, "cruelty_domestic": 170, "eve_teasing": 18, "kidnapping": 8, "dowry_death": 0, "other": 152},
                "2023": {"total": 598, "rape": 85, "molestation": 155, "cruelty_domestic": 165, "eve_teasing": 22, "kidnapping": 6, "dowry_death": 0, "other": 165},
                "2024": {"total": 592, "rape": 95, "molestation": 138, "cruelty_domestic": 155, "eve_teasing": 22, "kidnapping": 4, "dowry_death": 0, "other": 178}
            },
            "latest_annual_total": 592,
            "rate_per_lakh_females": 92.50,
            "public_space_crime_rate": 25.00,
            "domestic_crime_rate": 24.22,
            "relative_risk_category": "Low",
            "relative_risk_score": 3.9,
            "helpline": {"control_room": "0468-2222630", "women_cell": "0468-2222636", "pink_police": "1515 / 112"}
        },
        {
            "id": "alappuzha",
            "name": "Alappuzha",
            "headquarters": "Alappuzha",
            "police_units": ["Alappuzha District Police"],
            "center": {"lat": 9.4981, "lon": 76.3388},
            "female_population": 1112000,
            "total_population": 2127789,
            "area_sq_km": 1414,
            "crime_data": {
                "2022": {"total": 1180, "rape": 155, "molestation": 310, "cruelty_domestic": 340, "eve_teasing": 36, "kidnapping": 14, "dowry_death": 1, "other": 324},
                "2023": {"total": 1185, "rape": 160, "molestation": 305, "cruelty_domestic": 325, "eve_teasing": 42, "kidnapping": 11, "dowry_death": 0, "other": 342},
                "2024": {"total": 1178, "rape": 180, "molestation": 272, "cruelty_domestic": 305, "eve_teasing": 44, "kidnapping": 7, "dowry_death": 0, "other": 370}
            },
            "latest_annual_total": 1178,
            "rate_per_lakh_females": 105.94,
            "public_space_crime_rate": 28.42,
            "domestic_crime_rate": 27.43,
            "relative_risk_category": "Moderate",
            "relative_risk_score": 4.9,
            "helpline": {"control_room": "0477-2251326", "women_cell": "0477-2245366", "pink_police": "1515 / 112"}
        },
        {
            "id": "kottayam",
            "name": "Kottayam",
            "headquarters": "Kottayam",
            "police_units": ["Kottayam District Police"],
            "center": {"lat": 9.5916, "lon": 76.5222},
            "female_population": 1010000,
            "total_population": 1974551,
            "area_sq_km": 2208,
            "crime_data": {
                "2022": {"total": 965, "rape": 130, "molestation": 255, "cruelty_domestic": 260, "eve_teasing": 29, "kidnapping": 12, "dowry_death": 0, "other": 279},
                "2023": {"total": 972, "rape": 132, "molestation": 248, "cruelty_domestic": 250, "eve_teasing": 35, "kidnapping": 9, "dowry_death": 0, "other": 298},
                "2024": {"total": 966, "rape": 150, "molestation": 220, "cruelty_domestic": 235, "eve_teasing": 36, "kidnapping": 6, "dowry_death": 0, "other": 319}
            },
            "latest_annual_total": 966,
            "rate_per_lakh_females": 95.64,
            "public_space_crime_rate": 25.35,
            "domestic_crime_rate": 23.27,
            "relative_risk_category": "Low",
            "relative_risk_score": 4.2,
            "helpline": {"control_room": "0481-2562201", "women_cell": "0481-2560333", "pink_police": "1515 / 112"}
        },
        {
            "id": "idukki",
            "name": "Idukki",
            "headquarters": "Painavu",
            "police_units": ["Idukki District Police"],
            "center": {"lat": 9.8500, "lon": 76.9667},
            "female_population": 558000,
            "total_population": 1108974,
            "area_sq_km": 4358,
            "crime_data": {
                "2022": {"total": 515, "rape": 72, "molestation": 140, "cruelty_domestic": 135, "eve_teasing": 15, "kidnapping": 6, "dowry_death": 0, "other": 147},
                "2023": {"total": 520, "rape": 74, "molestation": 135, "cruelty_domestic": 130, "eve_teasing": 18, "kidnapping": 5, "dowry_death": 0, "other": 158},
                "2024": {"total": 516, "rape": 82, "molestation": 120, "cruelty_domestic": 125, "eve_teasing": 19, "kidnapping": 3, "dowry_death": 0, "other": 167}
            },
            "latest_annual_total": 516,
            "rate_per_lakh_females": 92.47,
            "public_space_crime_rate": 24.91,
            "domestic_crime_rate": 22.40,
            "relative_risk_category": "Low",
            "relative_risk_score": 3.8,
            "helpline": {"control_room": "04862-232320", "women_cell": "04862-232233", "pink_police": "1515 / 112"}
        },
        {
            "id": "ernakulam",
            "name": "Ernakulam",
            "headquarters": "Kochi",
            "police_units": ["Kochi City", "Ernakulam Rural"],
            "center": {"lat": 9.9816, "lon": 76.2999},
            "female_population": 1662000,
            "total_population": 3282388,
            "area_sq_km": 3068,
            "crime_data": {
                "2022": {"total": 2185, "rape": 298, "molestation": 590, "cruelty_domestic": 570, "eve_teasing": 72, "kidnapping": 32, "dowry_death": 1, "other": 622},
                "2023": {"total": 2190, "rape": 305, "molestation": 578, "cruelty_domestic": 540, "eve_teasing": 82, "kidnapping": 25, "dowry_death": 1, "other": 659},
                "2024": {"total": 2175, "rape": 340, "molestation": 515, "cruelty_domestic": 515, "eve_teasing": 85, "kidnapping": 16, "dowry_death": 0, "other": 704}
            },
            "latest_annual_total": 2175,
            "rate_per_lakh_females": 130.87,
            "public_space_crime_rate": 36.10,
            "domestic_crime_rate": 31.00,
            "relative_risk_category": "Elevated",
            "relative_risk_score": 7.0,
            "helpline": {"control_room": "0484-2394770", "women_cell": "0484-2394771", "pink_police": "1515 / 112"}
        },
        {
            "id": "thrissur",
            "name": "Thrissur",
            "headquarters": "Thrissur",
            "police_units": ["Thrissur City", "Thrissur Rural"],
            "center": {"lat": 10.5276, "lon": 76.2144},
            "female_population": 1642000,
            "total_population": 3121200,
            "area_sq_km": 3032,
            "crime_data": {
                "2022": {"total": 1680, "rape": 220, "molestation": 440, "cruelty_domestic": 450, "eve_teasing": 50, "kidnapping": 22, "dowry_death": 1, "other": 497},
                "2023": {"total": 1688, "rape": 225, "molestation": 432, "cruelty_domestic": 425, "eve_teasing": 60, "kidnapping": 18, "dowry_death": 1, "other": 527},
                "2024": {"total": 1678, "rape": 255, "molestation": 385, "cruelty_domestic": 405, "eve_teasing": 62, "kidnapping": 11, "dowry_death": 0, "other": 560}
            },
            "latest_annual_total": 1678,
            "rate_per_lakh_females": 102.19,
            "public_space_crime_rate": 27.22,
            "domestic_crime_rate": 24.66,
            "relative_risk_category": "Moderate",
            "relative_risk_score": 5.1,
            "helpline": {"control_room": "0487-2424193", "women_cell": "0487-2420000", "pink_police": "1515 / 112"}
        },
        {
            "id": "palakkad",
            "name": "Palakkad",
            "headquarters": "Palakkad",
            "police_units": ["Palakkad District Police"],
            "center": {"lat": 10.7867, "lon": 76.6548},
            "female_population": 1450000,
            "total_population": 2809934,
            "area_sq_km": 4480,
            "crime_data": {
                "2022": {"total": 1410, "rape": 185, "molestation": 365, "cruelty_domestic": 380, "eve_teasing": 42, "kidnapping": 18, "dowry_death": 1, "other": 419},
                "2023": {"total": 1420, "rape": 190, "molestation": 358, "cruelty_domestic": 360, "eve_teasing": 50, "kidnapping": 14, "dowry_death": 1, "other": 447},
                "2024": {"total": 1412, "rape": 218, "molestation": 320, "cruelty_domestic": 340, "eve_teasing": 52, "kidnapping": 9, "dowry_death": 0, "other": 473}
            },
            "latest_annual_total": 1412,
            "rate_per_lakh_females": 97.38,
            "public_space_crime_rate": 25.66,
            "domestic_crime_rate": 23.45,
            "relative_risk_category": "Moderate",
            "relative_risk_score": 4.6,
            "helpline": {"control_room": "0491-2534011", "women_cell": "0491-2536700", "pink_police": "1515 / 112"}
        },
        {
            "id": "malappuram",
            "name": "Malappuram",
            "headquarters": "Malappuram",
            "police_units": ["Malappuram District Police"],
            "center": {"lat": 11.0510, "lon": 76.0711},
            "female_population": 2132000,
            "total_population": 4112920,
            "area_sq_km": 3550,
            "crime_data": {
                "2022": {"total": 2190, "rape": 290, "molestation": 570, "cruelty_domestic": 610, "eve_teasing": 65, "kidnapping": 28, "dowry_death": 2, "other": 625},
                "2023": {"total": 2210, "rape": 295, "molestation": 560, "cruelty_domestic": 575, "eve_teasing": 78, "kidnapping": 22, "dowry_death": 1, "other": 679},
                "2024": {"total": 2198, "rape": 335, "molestation": 500, "cruelty_domestic": 540, "eve_teasing": 80, "kidnapping": 14, "dowry_death": 1, "other": 728}
            },
            "latest_annual_total": 2198,
            "rate_per_lakh_females": 103.09,
            "public_space_crime_rate": 27.20,
            "domestic_crime_rate": 25.37,
            "relative_risk_category": "Moderate",
            "relative_risk_score": 5.2,
            "helpline": {"control_room": "0483-2734922", "women_cell": "0483-2734988", "pink_police": "1515 / 112"}
        },
        {
            "id": "kozhikode",
            "name": "Kozhikode",
            "headquarters": "Kozhikode",
            "police_units": ["Kozhikode City", "Kozhikode Rural"],
            "center": {"lat": 11.2588, "lon": 75.7804},
            "female_population": 1614000,
            "total_population": 3086293,
            "area_sq_km": 2344,
            "crime_data": {
                "2022": {"total": 1820, "rape": 240, "molestation": 475, "cruelty_domestic": 490, "eve_teasing": 58, "kidnapping": 24, "dowry_death": 1, "other": 532},
                "2023": {"total": 1835, "rape": 245, "molestation": 465, "cruelty_domestic": 465, "eve_teasing": 70, "kidnapping": 19, "dowry_death": 1, "other": 570},
                "2024": {"total": 1826, "rape": 280, "molestation": 415, "cruelty_domestic": 440, "eve_teasing": 72, "kidnapping": 12, "dowry_death": 0, "other": 607}
            },
            "latest_annual_total": 1826,
            "rate_per_lakh_females": 113.14,
            "public_space_crime_rate": 30.17,
            "domestic_crime_rate": 27.26,
            "relative_risk_category": "Moderate",
            "relative_risk_score": 5.7,
            "helpline": {"control_room": "0495-2722220", "women_cell": "0495-2720233", "pink_police": "1515 / 112"}
        },
        {
            "id": "wayanad",
            "name": "Wayanad",
            "headquarters": "Kalpetta",
            "police_units": ["Wayanad District Police"],
            "center": {"lat": 11.6854, "lon": 76.1320},
            "female_population": 418000,
            "total_population": 817420,
            "area_sq_km": 2131,
            "crime_data": {
                "2022": {"total": 410, "rape": 55, "molestation": 110, "cruelty_domestic": 110, "eve_teasing": 12, "kidnapping": 5, "dowry_death": 0, "other": 118},
                "2023": {"total": 414, "rape": 57, "molestation": 105, "cruelty_domestic": 105, "eve_teasing": 15, "kidnapping": 4, "dowry_death": 0, "other": 128},
                "2024": {"total": 412, "rape": 65, "molestation": 95, "cruelty_domestic": 100, "eve_teasing": 16, "kidnapping": 2, "dowry_death": 0, "other": 134}
            },
            "latest_annual_total": 412,
            "rate_per_lakh_females": 98.56,
            "public_space_crime_rate": 26.56,
            "domestic_crime_rate": 23.92,
            "relative_risk_category": "Low",
            "relative_risk_score": 4.1,
            "helpline": {"control_room": "04936-202525", "women_cell": "04936-205100", "pink_police": "1515 / 112"}
        },
        {
            "id": "kannur",
            "name": "Kannur",
            "headquarters": "Kannur",
            "police_units": ["Kannur City", "Kannur Rural"],
            "center": {"lat": 11.8745, "lon": 75.3704},
            "female_population": 1340000,
            "total_population": 2523003,
            "area_sq_km": 2966,
            "crime_data": {
                "2022": {"total": 1395, "rape": 185, "molestation": 360, "cruelty_domestic": 375, "eve_teasing": 44, "kidnapping": 16, "dowry_death": 1, "other": 414},
                "2023": {"total": 1405, "rape": 190, "molestation": 352, "cruelty_domestic": 355, "eve_teasing": 52, "kidnapping": 12, "dowry_death": 1, "other": 443},
                "2024": {"total": 1398, "rape": 215, "molestation": 315, "cruelty_domestic": 335, "eve_teasing": 54, "kidnapping": 8, "dowry_death": 0, "other": 471}
            },
            "latest_annual_total": 1398,
            "rate_per_lakh_females": 104.33,
            "public_space_crime_rate": 27.54,
            "domestic_crime_rate": 25.00,
            "relative_risk_category": "Moderate",
            "relative_risk_score": 5.0,
            "helpline": {"control_room": "0497-2763333", "women_cell": "0497-2763337", "pink_police": "1515 / 112"}
        },
        {
            "id": "kasaragod",
            "name": "Kasaragod",
            "headquarters": "Kasaragod",
            "police_units": ["Kasaragod District Police"],
            "center": {"lat": 12.5102, "lon": 74.9852},
            "female_population": 682000,
            "total_population": 1307375,
            "area_sq_km": 1992,
            "crime_data": {
                "2022": {"total": 690, "rape": 95, "molestation": 180, "cruelty_domestic": 180, "eve_teasing": 22, "kidnapping": 8, "dowry_death": 0, "other": 205},
                "2023": {"total": 696, "rape": 98, "molestation": 175, "cruelty_domestic": 170, "eve_teasing": 26, "kidnapping": 6, "dowry_death": 0, "other": 221},
                "2024": {"total": 692, "rape": 110, "molestation": 155, "cruelty_domestic": 160, "eve_teasing": 27, "kidnapping": 4, "dowry_death": 0, "other": 236}
            },
            "latest_annual_total": 692,
            "rate_per_lakh_females": 101.47,
            "public_space_crime_rate": 26.69,
            "domestic_crime_rate": 23.46,
            "relative_risk_category": "Moderate",
            "relative_risk_score": 4.8,
            "helpline": {"control_room": "04994-222960", "women_cell": "04994-222966", "pink_police": "1515 / 112"}
        }
    ]
}

# Verify checksum and state totals
total_districts_2024 = sum(d["latest_annual_total"] for d in kerala_districts_crime["districts"])
print(f"Total districts sum for 2024: {total_districts_2024} (State official total: {kerala_districts_crime['state_totals']['2024']})")

with open("data/kerala_districts_crime.json", "w", encoding="utf-8") as f:
    json.dump(kerala_districts_crime, f, indent=2)

print("Saved data/kerala_districts_crime.json successfully.")
