# Healthcare Facility Access Gap Analysis

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Geospatial tool mapping healthcare accessibility across Nigerian states using road-network travel-time analysis, population density, and facility location data, identifying underserved communities and recommending optimal sites for new clinics.

---

## Problem Statement

Over 70 million Nigerians lack access to a functional health facility within reasonable travel time. State health ministries need spatial evidence to prioritise facility construction and mobile health unit deployment.

---

## Features

| Feature | Description |
|---------|-------------|
| Travel-Time Modelling | Network-based travel time per population cluster |
| Access Classification | Excellent / Good / Acceptable / Poor / Critical Gap |
| Population Quantification | People without adequate access per state |
| Optimal Site Recommendations | Top 10 priority locations for new facilities |
| Interactive Maps | Folium maps with access levels, facility markers, and recommended sites |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Geospatial | GeoPandas, Folium, Shapely |
| Analysis | pandas, NumPy, scikit-learn |
| Visualisation | Matplotlib, Seaborn, Plotly |

---

## Project Structure

```
healthcare-access-gap-analysis/
├── src/
│   ├── data_loader.py     # Population cluster and facility data ingestion
│   ├── analysis.py        # Travel-time modelling, gap scoring, recommendations
│   └── visualize.py       # Access maps, coverage charts
├── data/raw/              # Population rasters, facility locations, road network
├── outputs/               # Maps and recommendation reports
├── config.py              # Speed profiles, access thresholds
├── main.py                # Pipeline entry point
└── requirements.txt
```

---

## Quick Start

```bash
git clone https://github.com/Momahmoses/healthcare-access-gap-analysis.git
cd healthcare-access-gap-analysis
pip install -r requirements.txt
python main.py
```

---

## Data Sources

- GRID3 Nigeria healthcare facility locations
- WorldPop gridded population (100m resolution)
- OpenStreetMap Nigeria road network
- HMIS Primary Health Care registry

---

## Author

**Momah Moses**, Geospatial AI Engineer & Data Scientist
[GitHub](https://github.com/Momahmoses) · [Portfolio](https://momahmoses-ng-gis-portfolio.hf.space)
