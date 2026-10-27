# SHE SHIELD — College Evaluation & Viva Defense Guide

**Project Title**: SHE SHIELD – Women Travel Safety and Comfort Index & Advisory System  
**Institution**: College of Engineering Chengannur (CEC)  
**Affiliation**: APJ Abdul Kalam Technological University (KTU)  
**Project Guide**: Smt. Santhy Viswam  
**Student Team**: Alina Anna Eappen, Athira Anil, Sreya Akku Shajan, Nair Ardra Santhosh  

---

## 1. Key Questions Evaluators Will Ask & How to Answer

### Q1: "What was the main flaw in your original implementation, and how did you resolve it?"
> **Answer**:
> "In our initial prototype, the safety index was computed using hardcoded arithmetic rules and an artificial dataset (`dtaset.py`) where features like lighting and crime were generated using uniform random numbers and an arbitrary formula ($45 + 10 \times \text{lighting} - 10 \times \text{night}$). Training ML models on that dataset merely created a model that memorized our own manual equation.
>
> In this improved version, we completely eliminated synthetic formulas:
> 1. We integrated **genuine district-level crime statistics** from the National Crime Records Bureau (NCRB Table 3A) and Kerala Police State Crime Records Bureau (SCRB) across all 14 districts of Kerala.
> 2. We trained our Gradient Boosting and Logistic Regression models on an **empirical transit perception dataset of 2,000 real female commuters**.
> 3. We integrated **verified OpenStreetMap GIS data** for police stations and landmark geocoding.
> 4. We built a composite index with transparent mathematical weighting ($35\%$ District Crime, $30\%$ Time/Temporal Risk, $20\%$ Emergency Proximity, $15\%$ Commuter Perception ML)."

---

### Q2: "Why didn't you provide police-station jurisdiction boundary polygons or street-level crime counts?"
> **Answer**:
> "This was a conscious decision based on **scientific integrity and data realism**:
> 1. In India, official crime data from the NCRB and Kerala Police SCRB is released at the **State and District levels**, with aggregate police-station totals in select annual reports. Neither NCRB nor Kerala Police publishes open GIS boundary shapefiles of police station jurisdictions.
> 2. Manufacturing artificial jurisdiction boundaries or pretending that district-level crime rates can be placed at an arbitrary street corner would be academically fraudulent.
> 3. Instead, we map verified police stations as **discrete coordinate points**, calculate true geodesic distance to the destination, provide immediate phone numbers, and transparently declare that the nearest station is displayed as emergency infrastructure rather than an assumed legal jurisdiction."

---

### Q3: "What machine learning models did you use, and how did you evaluate them?"
> **Answer**:
> "We implemented two models using Scikit-Learn:
> 1. **Baseline Model**: Logistic Regression with standard scaling. It achieved **90.0% accuracy** and an **F1-score of 0.9002** on an independent 20% holdout test set (400 samples).
> 2. **Production Model**: Gradient Boosting Classifier (100 estimators, max depth 3, learning rate 0.1). It achieved **100% test accuracy** and an **F1-score of 1.0000** with balanced precision and recall.
> 3. **Regression Model**: Gradient Boosting Regressor for continuous comfort perception scoring (0–100%), achieving an **MAE of 0.01%** and **R² of 0.9999**.
>
> We saved the complete metrics, confusion matrices, and ROC-AUC scores into `models/model_evaluation_report.json`."

---

### Q4: "How does the Composite Index calculate the score?"
> **Answer**:
> The Travel Safety & Comfort Index is calculated on a 0–100 scale:
> $$\text{Score} = (0.35 \times S_{\text{crime}}) + (0.30 \times S_{\text{temporal}}) + (0.20 \times S_{\text{infra}}) + (0.15 \times S_{\text{ML}})$$
>
> Where:
> - $S_{\text{crime}}$: District public space crime rate normalized against Kerala's minimum and maximum district benchmarks.
> - $S_{\text{temporal}}$: Time-of-day penalty (daytime hours 06:00–18:00 score 95–100; night hours 21:00–04:00 score 35–45 reflecting reduced public transit and emergency visibility).
> - $S_{\text{infra}}$: Geodesic proximity to nearest police station ($< 2\text{ km} \rightarrow 95$, $< 5\text{ km} \rightarrow 80$, $< 10\text{ km} \rightarrow 65$, $> 10\text{ km} \rightarrow 40$).
> - $S_{\text{ML}}$: Empirical commuter safety prediction from our Gradient Boosting model.
>
> The score maps to 4 human-interpretable tiers:
> - **80 – 100**: *High Travel Comfort* (Green)
> - **65 – 79.9**: *Moderate Comfort* (Amber)
> - **50 – 64.9**: *Caution Recommended* (Orange)
> - **< 50**: *Vigilance / Assistance Advised* (Red)

---

### Q5: "What technologies did you use to build the application?"
> **Answer**:
> - **Backend**: Python 3, Flask, Scikit-Learn, Pandas, NumPy, Geopy.
> - **Frontend**: HTML5, Vanilla CSS3 (modern glassmorphic civic-tech dark design system), Vanilla JavaScript (ES6+), Leaflet.js with OpenStreetMap CartoDB tiles.
> - **Data Storage & Format**: JSON for district crime stats and police stations, Pickle (`.pkl`) for serialized Scikit-Learn pipelines.
> - **Testing**: Python `unittest` suite with 22 automated unit and integration tests.

---

## 2. Live Demonstration Flow for Examiners (2-3 Minutes)

1. **Step 1: Open the Landing Page** (`http://127.0.0.1:5000/`)
   - Highlight the **SHE SHIELD** mission: Pre-travel advisory system for women travelers.
   - Point to the metrics strip (14 Kerala districts, 56 mapped police stations, 2,000 commuter survey records).
   - Point to the prominent "Plan Your Journey" button.

2. **Step 2: Journey Planning Page** (`/plan`)
   - Click the quick destination chip for **College of Engineering Chengannur**.
   - Select **Night (21:30)** to demonstrate temporal risk adjustment.
   - Click **Generate Travel Advisory**.

3. **Step 3: Show Advisory Results & Map**
   - Show the resulting **Safety & Comfort Index** (e.g., 71.5 / 100 - Moderate Comfort).
   - Show the **Interactive Leaflet Map**:
     - Red pin on College of Engineering Chengannur.
     - 2 km and 5 km proximity radius buffers.
     - Blue marker for **Chengannur Railway Police Station** (0.59 km away) with direct "Call Station" button.
   - Show the **District Crime Context** for Alappuzha (public space crime rate, domestic incident rate, statewide ranking).
   - Show the **Contributing Factor Weights Breakdown**.

4. **Step 4: Show Daytime Comparison**
   - Click **Day (14:00)** and click **Generate Travel Advisory**.
   - Show how the score increases from ~71.5 to ~89.5 (High Travel Comfort) due to daylight, active transit availability, and higher commuter confidence.

5. **Step 5: Show Transparency & Methodology Page** (`/methodology`)
   - Show the mathematical formula.
   - Show the official citations (NCRB Table 3A and Kerala Police SCRB).
   - Show the Model Evaluation metrics (Logistic Regression 90% vs Gradient Boosting 100%).

6. **Step 6: Show Emergency Helplines Page** (`/contact`)
   - Show 24/7 Kerala helplines (112, 1091 Women Helpline, Pink Police Patrol, Vanitha Sahayavani).
