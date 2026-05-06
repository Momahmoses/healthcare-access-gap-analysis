import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SAMPLE_DIR = os.path.join(DATA_DIR, "sample")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

STUDY_STATES = {
    "Kano": {"lat": 12.0022, "lon": 8.5920},
    "Ogun": {"lat": 6.9980, "lon": 3.4737},
    "Borno": {"lat": 11.8333, "lon": 13.1500},
    "Rivers": {"lat": 4.8396, "lon": 6.9112},
    "Sokoto": {"lat": 13.0600, "lon": 5.2390},
}

# Travel time thresholds (minutes)
TRAVEL_TIME_THRESHOLDS = {
    "excellent": 15,
    "good": 30,
    "acceptable": 60,
    "poor": 120,
}

POPULATION_GRID_RES_KM = 1.0
FACILITY_TYPES = ["primary_health_centre", "general_hospital", "specialist_hospital", "mobile_clinic"]
