"""
Generate interactive Leaflet maps for college campus locations.

Scans one or more image folders for geotagged JPGs, extracts GPS coordinates,
and produces a Folium HTML map saved to the output/ directory.

Usage:
    # Map a single location
    python src/map_generator.py --folder images/admission_block --output output/admission_map.html

    # Map all locations (default)
    python src/map_generator.py

    # Map specific locations
    python src/map_generator.py --folders admission_block football_court parking basement
"""

import argparse
import os
import sys

import folium

# Allow running from project root
sys.path.insert(0, os.path.dirname(__file__))
from gps_utils import process_images

# Default image sub-folders (relative to project root images/)
DEFAULT_LOCATIONS = [
    'admission_block',
    'football_court',
    'parking',
    'basement',
    'main_ground',
]

# Colour per location for map marker differentiation
LOCATION_COLORS = {
    'admission_block': 'blue',
    'football_court':  'green',
    'parking':         'orange',
    'basement':        'red',
    'main_ground':     'purple',
}


def create_map(df, output_path='output/map.html'):
    """
    Create a Folium map with one marker per image and save as HTML.

    Args:
        df (pd.DataFrame): Must have columns ['filename', 'latitude', 'longitude']
                           and optionally 'location'.
        output_path (str): Destination HTML file path.
    """
    if df.empty:
        print("No GPS data found — map not created.")
        return

    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()

    m = folium.Map(location=[center_lat, center_lon], zoom_start=18)

    for _, row in df.iterrows():
        location = row.get('location', 'unknown')
        color = LOCATION_COLORS.get(location, 'gray')

        popup_text = f"<b>{row['filename']}</b><br>Location: {location}"

        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_text, max_width=250),
            icon=folium.Icon(color=color),
            tooltip=row['filename'],
        ).add_to(m)

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    m.save(output_path)
    print(f"Map saved → {output_path}  ({len(df)} markers)")


def main():
    parser = argparse.ArgumentParser(description='Generate campus GPS map from geotagged images.')
    parser.add_argument(
        '--folder', type=str, default=None,
        help='Single image folder path (overrides --folders).'
    )
    parser.add_argument(
        '--folders', nargs='+', default=DEFAULT_LOCATIONS,
        help='Sub-folder names inside images/ to include (default: all).'
    )
    parser.add_argument(
        '--images-dir', type=str, default='images',
        help='Root images directory (default: images/).'
    )
    parser.add_argument(
        '--output', type=str, default='output/map.html',
        help='Output HTML file path (default: output/map.html).'
    )
    args = parser.parse_args()

    import pandas as pd

    if args.folder:
        df = process_images(args.folder)
        df['location'] = os.path.basename(args.folder)
        all_data = [df] if not df.empty else []
    else:
        all_data = []
        for loc in args.folders:
            folder_path = os.path.join(args.images_dir, loc)
            df = process_images(folder_path)
            if not df.empty:
                df['location'] = loc
                all_data.append(df)

    if not all_data:
        print("No GPS data found in any folder. Exiting.")
        sys.exit(1)

    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"Total images with GPS: {len(combined_df)}")
    create_map(combined_df, output_path=args.output)


if __name__ == '__main__':
    main()
