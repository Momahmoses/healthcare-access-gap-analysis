"""Visualize healthcare access gaps with Folium maps and charts."""

import folium
from folium.plugins import MarkerCluster
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import OUTPUTS_DIR

ACCESS_COLORS = {
    "excellent": "#27ae60",
    "good": "#2ecc71",
    "acceptable": "#f39c12",
    "poor": "#e74c3c",
    "critical_gap": "#8e44ad",
}
FACILITY_COLORS = {
    "primary_health_centre": "blue",
    "general_hospital": "green",
    "specialist_hospital": "red",
    "mobile_clinic": "orange",
}


def create_access_map(pop_gdf: gpd.GeoDataFrame, fac_gdf: gpd.GeoDataFrame, recommended=None):
    center = [pop_gdf["latitude"].mean(), pop_gdf["longitude"].mean()]
    m = folium.Map(location=center, zoom_start=7, tiles="CartoDB positron")

    pop_cluster = MarkerCluster(name="Population Points").add_to(m)
    for _, row in pop_gdf.iterrows():
        level = row.get("access_level", "acceptable")
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4 + np.log1p(row["population"]) * 0.5,
            color=ACCESS_COLORS.get(level, "gray"),
            fill=True, fill_opacity=0.6,
            popup=folium.Popup(
                f"State: {row['state']}<br>Pop: {row['population']:,}<br>"
                f"Nearest: {row['nearest_facility_km']:.1f}km<br>"
                f"Travel: {row['travel_time_min']:.0f}min<br>Access: {level}",
                max_width=220,
            ),
        ).add_to(pop_cluster)

    fac_layer = folium.FeatureGroup(name="Healthcare Facilities").add_to(m)
    for _, row in fac_gdf[fac_gdf["is_functional"] == 1].iterrows():
        folium.Marker(
            location=[row["latitude"], row["longitude"]],
            popup=f"<b>{row['facility_type'].replace('_',' ').title()}</b><br>"
                  f"State: {row['state']}<br>Beds: {row['beds']}",
            icon=folium.Icon(color=FACILITY_COLORS.get(row["facility_type"], "gray"),
                             icon="plus-sign"),
        ).add_to(fac_layer)

    if recommended is not None:
        rec_layer = folium.FeatureGroup(name="Recommended New Sites").add_to(m)
        for _, row in recommended.iterrows():
            folium.Marker(
                location=[row["latitude"], row["longitude"]],
                popup=f"<b>Recommended Site</b><br>State: {row['state']}<br>Pop served: {row['population']:,}",
                icon=folium.Icon(color="black", icon="star"),
            ).add_to(rec_layer)

    legend_html = """
    <div style="position:fixed;bottom:30px;left:30px;z-index:1000;background:white;
                padding:12px;border-radius:8px;box-shadow:2px 2px 6px rgba(0,0,0,0.3);font-size:12px;">
    <b>Healthcare Access Level</b><br>
    <span style="color:#27ae60;">&#9632;</span> Excellent (&lt;15 min)<br>
    <span style="color:#2ecc71;">&#9632;</span> Good (15-30 min)<br>
    <span style="color:#f39c12;">&#9632;</span> Acceptable (30-60 min)<br>
    <span style="color:#e74c3c;">&#9632;</span> Poor (60-120 min)<br>
    <span style="color:#8e44ad;">&#9632;</span> Critical Gap (&gt;120 min)
    </div>"""
    m.get_root().html.add_child(folium.Element(legend_html))
    folium.LayerControl().add_to(m)

    os.makedirs(OUTPUTS_DIR, exist_ok=True)
    out = os.path.join(OUTPUTS_DIR, "healthcare_access_map.html")
    m.save(out)
    print(f"Access map saved → {out}")


def plot_access_summary(summary_df: pd.DataFrame):
    pivot = summary_df.pivot_table(
        index="state", columns="access_level", values="coverage_pct", aggfunc="sum"
    ).fillna(0)
    order = ["excellent", "good", "acceptable", "poor", "critical_gap"]
    cols = [c for c in order if c in pivot.columns]
    pivot = pivot[cols]

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = [ACCESS_COLORS[c] for c in cols]
    pivot.plot(kind="bar", ax=ax, color=colors, width=0.7)
    ax.set_ylabel("% of State Population")
    ax.set_title("Healthcare Access Level Distribution by State")
    ax.legend(title="Access Level", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.tick_params(axis="x", rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUTS_DIR, "access_summary_chart.png"), dpi=150)
    plt.close()
    print("Access summary chart saved.")
