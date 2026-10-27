# Data Compilation & Ingestion Scripts

This directory contains standalone Python pipelines used to gather, verify, and structure the primary datasets used by **SHE SHIELD**:

1. `compile_crime_data.py`:
   - Compiles official Kerala Police SCRB (State Crime Records Bureau) & NCRB Crime in India (2020–2024/2026) district-level crime statistics.
   - Calculates public space crime rates, domestic incident rates, and statewide benchmark rankings for all 14 districts.
   - Outputs: `data/kerala_districts_crime.json`

2. `compile_police_stations.py`:
   - Gathers verified police stations across Kerala with latitude, longitude, official station landline phone numbers, district associations, and special women-cell tags.
   - Outputs: `data/kerala_police_stations.json`

3. `compile_gazetteer.py`:
   - Builds an offline Kerala gazetteer of 65 major transit hubs, bus stands, railway stations, and colleges (including College of Engineering Chengannur) for resilient zero-latency geocoding.
   - Outputs: `data/gazetteer_kerala.json`
