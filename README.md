🛡️ SHE SHIELD

Women Travel Safety & Comfort Index and Advisory System

«A data-driven pre-travel decision-support system designed to help women assess the safety and comfort of a destination before travelling.»

SHE SHIELD is a machine-learning-based Women Travel Safety & Comfort Index and Advisory System developed as an academic project at the College of Engineering Chengannur (CEC).

Instead of functioning as an emergency-response or real-time tracking application, SHE SHIELD focuses on a different question:

“How suitable and safe might this location be for travelling at a particular time?”

The system evaluates contextual factors around a selected location and provides a safety probability along with an easy-to-understand advisory.

---

🌍 Problem Statement

Travel safety can depend on several contextual factors beyond the destination itself.

The availability of nearby emergency services, transportation facilities, accommodation, shops, street infrastructure and other points of interest can influence how comfortable a traveller may feel in an unfamiliar location.

However, travellers often lack a simple way to evaluate these factors before beginning a journey.

SHE SHIELD addresses this gap by combining:

- Location-based contextual information
- OpenStreetMap data
- Geospatial feature extraction
- Machine learning
- An interactive map-based interface

to generate a pre-travel safety and comfort assessment.

---

💡 What SHE SHIELD Does

The system allows a user to provide a location and relevant travel context.

It then:

1. 📍 Identifies and geocodes the selected location.
2. 🗺️ Retrieves relevant surrounding geographical information.
3. 🏥 Examines contextual features such as nearby hospitals and police stations.
4. 🚏 Considers surrounding infrastructure and points of interest such as bus stops, hotels, shops and streetlights.
5. 🤖 Processes the extracted features through a trained machine-learning model.
6. 📊 Generates a safety probability.
7. 💬 Converts the result into a simple advisory category.

Safety Categories

Safety Probability| Advisory
Below 40%| 🔴 Unsafe
40% – 70%| 🟡 Cautious
Above 70%| 🟢 Safe

These categories are intended as decision-support indicators, not guarantees of real-world safety.

---

🔄 System Workflow

User Input
    │
    ▼
Location Identification
    │
    ▼
Geocoding using Nominatim
    │
    ▼
OpenStreetMap / Overpass Data Retrieval
    │
    ▼
Geospatial Feature Extraction
    │
    ├── Police Stations
    ├── Hospitals
    ├── Streetlights
    ├── Bus Stops
    ├── Hotels
    ├── Shops / POIs
    └── Other Contextual Features
    │
    ▼
Feature Processing
    │
    ▼
Machine Learning Model
    │
    ▼
Safety Probability
    │
    ▼
Safety Category & Advisory
    │
    ▼
Interactive Map-Based Result

---

🤖 Machine Learning Approach

The project experimented with multiple classification approaches to identify a suitable model for the safety assessment task.

Models explored

- Logistic Regression
- Gradient Boosting Classifier

The final implementation uses a Gradient Boosting Classifier for the safety assessment.

The trained model is stored as:

safety_model.pkl

The model produces a probability-based output, which is then mapped to the three advisory categories.

---

🗺️ Data & Geospatial Processing

SHE SHIELD uses open geospatial data to derive contextual information about a location.

OpenStreetMap

OpenStreetMap provides geographical information about surrounding infrastructure and points of interest.

Relevant features are retrieved using:

- Nominatim — location geocoding
- Overpass API — querying OpenStreetMap data
- OSMnx — working with OpenStreetMap-based geospatial data

Examples of contextual information include:

- Police stations
- Hospitals
- Bus stops
- Hotels
- Shops
- Streetlight-related infrastructure
- Other nearby points of interest

The extracted information is transformed into features that can be used by the machine-learning model.

---

🖥️ Application

The project is implemented as a Flask-based web application.

The application provides pages/features for:

- 🏠 Home
- 📍 Safety assessment
- 🗺️ Interactive map
- ℹ️ About
- 📞 Contact
- 💬 Feedback

The map visualization is implemented using Folium.

«Note: The project is currently available as source code and has not been deployed as a publicly hosted website.»

---

🛠️ Technology Stack

Programming Language

- Python

Backend

- Flask

Machine Learning

- Scikit-learn
- Logistic Regression
- Gradient Boosting Classifier

Data Processing

- Pandas
- NumPy

Geospatial Technologies

- OSMnx
- OpenStreetMap
- Nominatim
- Overpass API
- Folium

Development Tools

- Git
- GitHub

---

📁 Project Structure

SHE-SHIELD/
│
├── app.py
├── safety_model.pkl
├── requirements.txt
│
├── templates/
│   ├── index.html
│   ├── advisory.html
│   ├── about.html
│   ├── contact.html
│   └── feedback.html
│
├── static/
│   └── ...
│
├── notebooks/
│   └── ...
│
└── README.md

The exact structure may vary depending on the current repository version.

---

🚀 Getting Started

1. Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SHE-SHIELD

2. Create a virtual environment

python -m venv venv

Activate it:

Windows

venv\Scripts\activate

Linux / macOS

source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Run the application

python app.py


---

⚠️ Limitations

SHE SHIELD is a research and academic prototype, and its results should not be interpreted as a guarantee of personal safety.

Some important limitations include:

- OpenStreetMap data may be incomplete or outdated.
- Some locations may have missing infrastructure information.
- Results depend on the availability and quality of geospatial data.
- External API availability and usage limits can affect data retrieval.
- The system requires an internet connection for external map/geospatial services.
- A model-generated probability cannot capture every real-world safety factor.
- The system does not provide emergency response or real-time tracking.

Therefore, users should treat the output as one source of information for pre-travel planning, rather than a definitive safety assessment.

---

🔮 Future Scope

The project can be further extended through:

- Integration of larger and more diverse datasets
- Improved geospatial feature engineering
- More extensive model evaluation
- Real-time environmental and transportation information
- More comprehensive accessibility and infrastructure indicators
- Improved personalization based on travel context
- Mobile application development
- Deployment as a scalable cloud application
- Continuous model evaluation using newly available data

---

🎯 Project Focus

SHE SHIELD is built around the idea of proactive travel planning rather than emergency response.

The goal is not to tell someone whether they should or shouldn't visit a place.

Instead, it attempts to provide contextual information in a structured way so that travellers can make more informed decisions before starting their journey.

---

👩‍💻 Team

Project Team

- Alina Anna Eapen
- Athira Anil
- Sreya Akku Shajan
- Ardra Santhosh

Project Guide

Santhy Viswam

Institution

College of Engineering Chengannur (CEC)

---

📌 Project Status

Status: Academic Project / Prototype

The source code and implementation are available through this repository. The application is not currently hosted as a public website.

---

📄 Disclaimer

SHE SHIELD is developed for academic and research purposes.

The safety categories and probabilities generated by the system are computational estimates based on available contextual data. They should not be treated as guarantees of actual safety or as a substitute for personal judgement, official travel advisories, or emergency services.

---

⭐ Acknowledgements

We would like to thank our project guide, faculty members and the College of Engineering Chengannur for their guidance and support throughout the development of this project.


