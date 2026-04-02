"""
Convert campus images to a CSV dataset of flattened 64x64 grayscale pixels.

Reads all JPG images from the images/ directory (all sub-folders),
resizes each to 64×64 grayscale, flattens pixel values into a single row,
and writes the result to output/images_dataset.csv.

Usage:
    python src/image_to_csv.py
    python src/image_to_csv.py --images-dir images/ --output output/images_dataset.csv
"""

import argparse
import os
import sys

import cv2
import numpy as np
import pandas as pd


def collect_images(images_dir):
    """
    Recursively find all JPG files under images_dir.

    Args:
        images_dir (str): Root images directory.

    Returns:
        list[str]: Absolute paths to every .jpg file found.
    """
    jpg_paths = []
    for root, _, files in os.walk(images_dir):
        for file in files:
            if file.lower().endswith('.jpg'):
                jpg_paths.append(os.path.join(root, file))
    return sorted(jpg_paths)


def image_to_row(path, size=(64, 64)):
    """
    Load an image, convert to grayscale, resize, and flatten.

    Args:
        path (str): Path to image file.
        size (tuple): Target (width, height).

    Returns:
        np.ndarray | None: Flattened pixel array of length size[0]*size[1],
                           or None if the image could not be read.
    """
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Warning: Could not read image: {path}")
        return None
    img_resized = cv2.resize(img, size)
    return img_resized.flatten()


def build_dataset(images_dir, size=(64, 64)):
    """
    Build a DataFrame where each row is one image's flattened pixels.

    Args:
        images_dir (str): Root images directory.
        size (tuple): Resize target.

    Returns:
        pd.DataFrame: Columns are ['filepath'] + ['px_0', 'px_1', ..., 'px_N'].
    """
    paths = collect_images(images_dir)
    if not paths:
        print(f"No JPG images found in: {images_dir}")
        return pd.DataFrame()

    print(f"Found {len(paths)} images. Processing...")
    rows = []
    for path in paths:
        pixels = image_to_row(path, size)
        if pixels is not None:
            row = {'filepath': os.path.relpath(path)}
            for i, val in enumerate(pixels):
                row[f'px_{i}'] = val
            rows.append(row)

    print(f"Successfully processed {len(rows)} images.")
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(
        description='Generate grayscale pixel dataset CSV from campus images.'
    )
    parser.add_argument(
        '--images-dir', type=str, default='images',
        help='Root images directory (default: images/).'
    )
    parser.add_argument(
        '--output', type=str, default='output/images_dataset.csv',
        help='Output CSV path (default: output/images_dataset.csv).'
    )
    parser.add_argument(
        '--size', type=int, nargs=2, default=[64, 64], metavar=('W', 'H'),
        help='Resize dimensions width height (default: 64 64).'
    )
    args = parser.parse_args()

    df = build_dataset(args.images_dir, size=tuple(args.size))
    if df.empty:
        sys.exit(1)

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Dataset saved → {args.output}  ({len(df)} rows, {len(df.columns)} columns)")


if __name__ == '__main__':
    main()
