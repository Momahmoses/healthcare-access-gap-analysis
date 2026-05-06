# Healthcare Facility Access Gap Analysis

A geospatial tool that maps healthcare accessibility across Nigerian states using road network travel-time analysis, population density, and facility location data — identifying underserved communities and recommending optimal sites for new clinics.

## Overview

Uses network-based travel time modeling to:
- Calculate access time from every population cluster to the nearest functional healthcare facility
- Classify communities by access level (Excellent / Good / Acceptable / Poor / Critical Gap)
- Quantify how many people lack adequate healthcare access per state
- Recommend top-priority locations for new facility placement

## Features

- **Population Mapping**: WorldPop-style gridded population data per state
- **Facility Database**: Primary Health Centres, General Hospitals, Specialist Hospitals, Mobile Clinics
- **Travel Time Analysis**: Distance-based travel time (urban vs rural speed assumptions)
- **Gap Scoring**: Weighted population × travel-time gap score for priority ranking
- **Interactive Maps**: Folium maps with access levels, facility markers, and recommended sites
- **Recommendations**: Top 10 optimal new facility sites based on population need

## Project Structure

```
healthcare-access-gap-analysis/
├── src/
│   ├── data_ingestion.py     # Population grid & facility data generation
│   ├── access_analysis.py    # Travel time & gap analysis
│   └── visualization.py      # Folium maps & summary charts
├── data/sample/
├── outputs/
├── config.py
├── main.py
└── requirements.txt
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Target States

| State | Region | Focus |
|-------|--------|-------|
| Kano | Northwest | Dense urban + rural periphery |
| Ogun | Southwest | Peri-urban access gaps |
| Borno | Northeast | Conflict-affected access |
| Rivers | South-South | Delta community access |
| Sokoto | Northwest | Remote rural communities |

## Data Sources (Production)

- Population: WorldPop 100m gridded dataset
- Facilities: FMOH HMIS, HDX Health Facilities Nigeria
- Road Network: OpenStreetMap via OSMnx
- Travel Time: friction surface (Malaria Atlas Project)

## Author

**MOMAH MOSES .C.**  
Data Scientist & ML Engineer | [GitHub](https://github.com/Momahmoses)
