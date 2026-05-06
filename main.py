"""Main pipeline: Healthcare Facility Access Gap Analysis."""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from src.data_ingestion import generate_population_grid, generate_facilities, save_data
from src.access_analysis import compute_nearest_facility, gap_analysis, recommend_new_sites
from src.visualization import create_access_map, plot_access_summary


def main():
    print("=" * 60)
    print("  Healthcare Facility Access Gap Analysis")
    print("  States: Kano, Ogun, Borno, Rivers, Sokoto — Nigeria")
    print("=" * 60)

    print("\n[1/5] Generating population grid...")
    pop_gdf = generate_population_grid(n_points=3000)
    print(f"  {len(pop_gdf):,} population points | Total pop: {pop_gdf['population'].sum():,.0f}")

    print("\n[2/5] Generating healthcare facilities...")
    fac_gdf = generate_facilities(n_facilities=200)
    functional = fac_gdf[fac_gdf["is_functional"] == 1]
    print(f"  {len(fac_gdf)} facilities | {len(functional)} functional ({len(functional)/len(fac_gdf):.0%})")
    save_data(pop_gdf, fac_gdf)

    print("\n[3/5] Computing travel time to nearest facility...")
    pop_gdf = compute_nearest_facility(pop_gdf, fac_gdf)
    print(f"  Avg travel time: {pop_gdf['travel_time_min'].mean():.1f} min")
    print(f"  Max travel time: {pop_gdf['travel_time_min'].max():.1f} min")

    print("\n[4/5] Running gap analysis...")
    summary = gap_analysis(pop_gdf)
    recommended = recommend_new_sites(pop_gdf, n_sites=10)

    print("\n[5/5] Generating access maps...")
    create_access_map(pop_gdf, fac_gdf, recommended)
    plot_access_summary(summary)

    print("\n✓ Pipeline complete. Outputs saved to ./outputs/")


if __name__ == "__main__":
    main()
