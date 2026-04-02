"""
Shared GPS utility functions for the College Mapping project.
"""

import os
import exifread
import pandas as pd


def get_decimal_from_dms(dms, ref):
    """
    Convert GPS coordinates from DMS (Degrees, Minutes, Seconds) to decimal degrees.

    Args:
        dms: List of IFDRatio values [degrees, minutes, seconds]
        ref: Direction reference string ('N', 'S', 'E', 'W')

    Returns:
        float: Decimal degree coordinate (negative for South/West)
    """
    degrees = float(dms[0].num) / float(dms[0].den)
    minutes = float(dms[1].num) / float(dms[1].den)
    seconds = float(dms[2].num) / float(dms[2].den)

    decimal = degrees + minutes / 60 + seconds / 3600

    if ref in ['S', 'W']:
        decimal = -decimal

    return decimal


def process_images(folder):
    """
    Scan a folder for JPG images and extract GPS coordinates from EXIF data.

    Args:
        folder (str): Path to folder containing geotagged JPG images

    Returns:
        pd.DataFrame: DataFrame with columns ['filename', 'latitude', 'longitude']
                      Only includes images that have valid GPS data.
    """
    data = []

    if not os.path.isdir(folder):
        print(f"Warning: Folder not found: {folder}")
        return pd.DataFrame(columns=['filename', 'latitude', 'longitude'])

    for file in os.listdir(folder):
        if not file.lower().endswith('.jpg'):
            continue

        path = os.path.join(folder, file)

        with open(path, 'rb') as f:
            tags = exifread.process_file(f, details=False)

            if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                lat = get_decimal_from_dms(
                    tags['GPS GPSLatitude'].values,
                    tags['GPS GPSLatitudeRef'].printable
                )
                lon = get_decimal_from_dms(
                    tags['GPS GPSLongitude'].values,
                    tags['GPS GPSLongitudeRef'].printable
                )
                data.append({'filename': file, 'latitude': lat, 'longitude': lon})
            else:
                print(f"No GPS data: {file}")

    return pd.DataFrame(data, columns=['filename', 'latitude', 'longitude'])
