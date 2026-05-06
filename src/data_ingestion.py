"""Generate synthetic population grid and healthcare facility data."""

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import SAMPLE_DIR, STUDY_STATES, FACILITY_TYPES


def generate_population_grid(n_points: int = 3000, seed: int = 42) -> gpd.GeoDataFrame:
    rng = np.random.default_rng(seed)
    states = list(STUDY_STATES.keys())
    state_labels = rng.choice(states, size=n_points)
    lats, lons = [], []
    for s in state_labels:
        info = STUDY_STATES[s]
        offset = 0.7
        lats.append(info["lat"] + rng.uniform(-offset, offset))
        lons.append(info["lon"] + rng.uniform(-offset, offset))

    pop = rng.lognormal(7, 1.8, n_points).clip(50, 80000).astype(int)
    is_urban = (pop > 5000).astype(int)
    geometry = [Point(lon, lat) for lon, lat in zip(lons, lats)]
    df = pd.DataFrame({
        "state": state_labels, "latitude": lats, "longitude": lons,
        "population": pop, "is_urban": is_urban,
    })
    return gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")


def generate_facilities(n_facilities: int = 200, seed: int = 7) -> gpd.GeoDataFrame:
    rng = np.random.default_rng(seed)
    states = list(STUDY_STATES.keys())
    state_labels = rng.choice(states, size=n_facilities)
    lats, lons = [], []
    for s in state_labels:
        info = STUDY_STATES[s]
        offset = 0.6
        lats.append(info["lat"] + rng.uniform(-offset, offset))
        lons.append(info["lon"] + rng.uniform(-offset, offset))

    ftype_probs = [0.55, 0.30, 0.10, 0.05]
    ftypes = rng.choice(FACILITY_TYPES, size=n_facilities, p=ftype_probs)
    beds = {"primary_health_centre": 10, "general_hospital": 100,
            "specialist_hospital": 300, "mobile_clinic": 0}
    bed_counts = np.array([beds[f] + rng.integers(0, 30) for f in ftypes])

    df = pd.DataFrame({
        "state": state_labels, "latitude": lats, "longitude": lons,
        "facility_type": ftypes, "beds": bed_counts,
        "is_functional": rng.choice([1, 0], size=n_facilities, p=[0.78, 0.22]),
    })
    geometry = [Point(lon, lat) for lon, lat in zip(lons, lats)]
    return gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")


def save_data(pop_gdf: gpd.GeoDataFrame, fac_gdf: gpd.GeoDataFrame):
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    pop_gdf.drop(columns="geometry").to_csv(os.path.join(SAMPLE_DIR, "population_grid.csv"), index=False)
    fac_gdf.drop(columns="geometry").to_csv(os.path.join(SAMPLE_DIR, "facilities.csv"), index=False)
    print(f"Saved {len(pop_gdf):,} population points and {len(fac_gdf)} facilities.")
