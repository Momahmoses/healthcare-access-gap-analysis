"""Travel time and coverage gap analysis."""

import numpy as np
import pandas as pd
import geopandas as gpd
from scipy.spatial import cKDTree
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import TRAVEL_TIME_THRESHOLDS, OUTPUTS_DIR

# Average road speed assumptions (km/h) by area type
URBAN_SPEED_KMH = 25
RURAL_SPEED_KMH = 40


def compute_nearest_facility(pop_gdf: gpd.GeoDataFrame, fac_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Compute straight-line distance to nearest functional facility."""
    functional = fac_gdf[fac_gdf["is_functional"] == 1].reset_index(drop=True)
    pop_coords = np.radians(pop_gdf[["latitude", "longitude"]].values)
    fac_coords = np.radians(functional[["latitude", "longitude"]].values)
    tree = cKDTree(fac_coords)
    dists, idxs = tree.query(pop_coords, k=1)

    # Haversine approximation: 1 degree ≈ 111 km
    dist_km = dists * 6371 * np.pi / 180 * 180 / np.pi
    dist_km = dists * 111

    pop_gdf = pop_gdf.copy()
    pop_gdf["nearest_facility_km"] = dist_km
    pop_gdf["nearest_facility_type"] = functional.iloc[idxs]["facility_type"].values
    pop_gdf["travel_time_min"] = (dist_km / pop_gdf["is_urban"].map(
        {1: URBAN_SPEED_KMH, 0: RURAL_SPEED_KMH}
    ) * 60)
    return pop_gdf


def classify_access(travel_time_min: float) -> str:
    t = TRAVEL_TIME_THRESHOLDS
    if travel_time_min <= t["excellent"]:
        return "excellent"
    elif travel_time_min <= t["good"]:
        return "good"
    elif travel_time_min <= t["acceptable"]:
        return "acceptable"
    elif travel_time_min <= t["poor"]:
        return "poor"
    return "critical_gap"


def gap_analysis(pop_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    pop_gdf = pop_gdf.copy()
    pop_gdf["access_level"] = pop_gdf["travel_time_min"].apply(classify_access)
    underserved = pop_gdf[pop_gdf["access_level"].isin(["poor", "critical_gap"])]

    summary = (
        pop_gdf.groupby(["state", "access_level"])
        .agg(population=("population", "sum"), n_points=("population", "count"))
        .reset_index()
    )
    state_total = pop_gdf.groupby("state")["population"].sum().rename("total_population")
    summary = summary.merge(state_total, on="state")
    summary["coverage_pct"] = summary["population"] / summary["total_population"] * 100

    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    summary.to_csv(os.path.join(OUTPUTS_DIR, "access_gap_summary.csv"), index=False)
    print(f"\n  Population without adequate access (<30 min): "
          f"{underserved['population'].sum():,.0f} people")
    return summary


def recommend_new_sites(pop_gdf: gpd.GeoDataFrame, n_sites: int = 10) -> gpd.GeoDataFrame:
    """Identify top underserved clusters for new facility placement."""
    underserved = pop_gdf[pop_gdf["travel_time_min"] > 60].copy()
    underserved["score"] = underserved["population"] * underserved["travel_time_min"]
    top = underserved.nlargest(n_sites, "score")[["state", "latitude", "longitude", "population", "travel_time_min", "score"]]
    top.to_csv(os.path.join(OUTPUTS_DIR, "recommended_facility_sites.csv"), index=False)
    print(f"  Top {n_sites} recommended sites saved.")
    return top
