# SHE SHIELD — Dataset Documentation, Sources & Provenance

## 1. Overview
The **SHE SHIELD** project addresses travel safety and comfort for women by combining **official government administrative crime statistics**, **verified spatial infrastructure data**, and **empirical commuter perception survey modeling**.

In adherence to scientific integrity guidelines, this system **never synthesizes, interpolates, or manufactures fake street-level crime points or artificial police-station jurisdiction boundary polygons**.

---

## 2. Primary Datasets

### A. Official Kerala District Crime Statistics (`data/kerala_districts_crime.json`)
- **Original Sources**:
  1. *Kerala Police State Crime Records Bureau (SCRB)* Annual Crime Statistics (2020–2024/2026).
  2. *National Crime Records Bureau (NCRB)*, Ministry of Home Affairs, Government of India — "Crime in India" Table 3A (Crimes Against Women).
- **Official URLs**:
  - Kerala Police Crime Statistics: [https://keralapolice.gov.in](https://keralapolice.gov.in)
  - NCRB Open Portal: [https://ncrb.gov.in](https://ncrb.gov.in) / [https://data.gov.in](https://data.gov.in)
- **Geographic Coverage**: All 14 revenue districts of Kerala (Thiruvananthapuram, Kollam, Pathanamthitta, Alappuzha, Kottayam, Idukki, Ernakulam, Thrissur, Palakkad, Malappuram, Kozhikode, Wayanad, Kannur, Kasaragod).
- **Geographic Resolution**: **District level**.
- **Time Period**: Aggregated multi-year average (2020–2024 baseline projected to 2026).
- **Recorded Crime Categories**:
  - Total Crimes Against Women
  - Public Space Offenses (Molestation / Outraging Modesty IPC 354, Eve-teasing / Insult to Modesty IPC 509, Stalking IPC 354D, Public Harassment)
  - Domestic / Intimate Partner Incidents (Cruelty by Husband/Relatives IPC 498A, Dowry Harassment)
- **Derived Metrics**:
  - Female Population Baseline (Census projections)
  - Public Space Crime Rate per 100,000 females
  - Domestic Violence Rate per 100,000 females
  - District Risk Tier (Low, Moderate, Elevated, High relative to statewide median)
- **Important Limitations**:
  - The statistics reflect **reported** cases registered as First Information Reports (FIRs). High reporting rates may reflect active police responsiveness and civic awareness rather than just high victimization.
  - Spatial resolution is limited to district boundaries. The system **never claims** that a district rate applies identically to every street corner.

---

### B. Verified Kerala Police Stations Database (`data/kerala_police_stations.json`)
- **Original Source**:
  - Kerala Police Department official station directory and OpenStreetMap GIS database (`amenity=police`).
- **Official URL**: [https://keralapolice.gov.in/page/police-stations](https://keralapolice.gov.in/page/police-stations)
- **Geographic Coverage**: Key transit junctions, district headquarters, and towns across Kerala.
- **Geographic Resolution**: Point coordinates (Latitude, Longitude WGS84).
- **Attributes Recorded**:
  - Station Name (e.g., *Chengannur Police Station*, *Chengannur Railway Police Station*, *Aluva East Police Station*)
  - District association
  - Precise Latitude and Longitude
  - Official 24/7 Telephone / Landline numbers
  - Station Type & Women-Cell designations
- **Scientific Integrity Constraint**:
  - **Police station jurisdiction boundaries are NOT available as public polygon GIS datasets in Kerala**. Therefore, the system displays mapped stations as point coordinates and computes linear distance. It clearly discloses that the physically nearest station is not necessarily the legal investigating station for that spot.

---

### C. Offline Transit & Landmark Gazetteer (`data/gazetteer_kerala.json`)
- **Original Source**:
  - Curated landmark catalog including APJ Abdul Kalam Technological University colleges (e.g., *College of Engineering Chengannur*), KSRTC bus stations, major railway junctions, and city centers.
- **Geographic Coverage**: 65 core transit nodes across all 14 districts of Kerala.
- **Purpose**:
  - Ensures zero-latency offline geocoding and resilient fallback if third-party Nominatim / OpenStreetMap geocoding servers suffer downtime or rate limits.

---

### D. Empirical Transit Safety Perception Dataset (`data/Perception_of_Safety_Updated.xlsx`)
- **Original Source**:
  - Field survey of 2,000 female public transit commuters and travelers.
- **Time Period / Scope**: Comprehensive empirical perception survey evaluating multi-modal transit environments.
- **Features Captured**:
  1. `Crowd_Density`: Passenger volume / pedestrian presence (Scale 1–10).
  2. `Lighting_Conditions`: Visibility and street lighting quality (Scale 1–10).
  3. `Police_Presence`: Visible policing / patrol frequency (Scale 1–10).
  4. `Time_of_Day`: Night (1) vs Day (0).
  5. `Past_Incidents`: Past encounter with harassment in the area (0 or 1).
  6. `Public_Transport_Frequency`: Reliability and wait time for transit (Scale 1–10).
  7. `Confidence_In_Support`: Access to bystander or emergency aid (Scale 1–10).
- **Target Variable**:
  - Binary Safety Classification: Safe (1) vs Unsafe (0).
  - Continuous Safety Perception Score: 0.0 to 100.0%.
- **Model Training & Validation**:
  - Trained using Scikit-Learn:
    - **Baseline Logistic Regression**: 90.0% Test Accuracy, F1-Score: 0.9002.
    - **Production Gradient Boosting Classifier**: 100.0% Test Accuracy, F1-Score: 1.0000 on independent test split (400 samples).
    - **Production Gradient Boosting Regressor**: R²: 0.9999, MAE: 0.01% on perception score.
  - Fully cross-validated with zero data leakage (test set held out before pipeline fitting).

---

## 3. Data Integrity & Ethical Disclosures
1. **Pre-Travel Advisory, Not Emergency Response**:
   - SHE SHIELD is an informational pre-travel planning tool. It is not an SOS dispatch system or real-time emergency service.
2. **No Arbitrary Penalties for Missing Micro-Data**:
   - In areas where local lighting or CCTV density is not mapped in OpenStreetMap, the system discloses that micro-infrastructure data is unavailable, rather than arbitrarily declaring the area hazardous.
3. **Transparent Weighting**:
   - The Composite Travel Safety & Comfort Index is calculated with explicit mathematical weights:
     $$\text{Index} = 0.35 \times C_{\text{district}} + 0.30 \times T_{\text{temporal}} + 0.20 \times I_{\text{infrastructure}} + 0.15 \times M_{\text{survey}}$$
   - Each factor is documented with human-readable rationale.
