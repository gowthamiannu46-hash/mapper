# campus-gps-mapper

Interactive GPS map of a college campus built from geotagged photos.

Extracts GPS metadata from JPG images taken around campus and generates a Leaflet-based HTML map with colour-coded markers per location. Also includes a script to build a grayscale pixel dataset from the images for ML use.

---

## Project Structure

```
college-mapping/
├── src/
│   ├── gps_utils.py       # Shared GPS extraction helpers (DMS → decimal)
│   ├── map_generator.py   # Build interactive Folium map from image folders
│   └── image_to_csv.py    # Convert images to flattened grayscale CSV dataset
├── images/
│   ├── admission_block/   # Geotagged JPGs — Admission Block
│   ├── football_court/    # Geotagged JPGs — Football Court
│   ├── parking/           # Geotagged JPGs — Parking Area
│   ├── basement/          # Geotagged JPGs — Basement
│   └── main_ground/       # Geotagged JPGs — Main Ground
├── output/                # Generated files (gitignored)
│   ├── map.html           # Interactive campus map
│   └── images_dataset.csv # Pixel dataset
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Setup

```bash
git clone https://github.com/gowthamiannu46/campus-gps-mapper.git
cd campus-gps-mapper
pip install -r campus-gps-mapper

```

---

## Usage

### 1. Generate the Campus Map

Place your geotagged JPG photos inside the relevant sub-folder under `images/`, then run:

```bash
# Map all locations (default)
python src/map_generator.py

# Map a single location
python src/map_generator.py --folder images/admission_block --output output/admission_map.html

# Choose specific locations
python src/map_generator.py --folders admission_block football_court
```

Output: `output/map.html` — open in any browser.

### 2. Build the Image Dataset

```bash
python src/image_to_csv.py
```

Output: `output/images_dataset.csv` — one row per image, 4096 pixel columns (64×64 grayscale).

---

## Adding Images

Put your geotagged JPGs (taken with an app like **GPS Map Camera**) into the matching sub-folder:

| Campus Location   | Folder                    |
|-------------------|---------------------------|
| Admission Block   | `images/admission_block/` |
| Football Court    | `images/football_court/`  |
| Parking           | `images/parking/`         |
| Basement          | `images/basement/`        |
| Main Ground       | `images/main_ground/`     |

> **Note:** Images are excluded from version control via `.gitignore`.  
> Use [Git LFS](https://git-lfs.com/) if you need to store them in the repo.

---

## Dependencies

| Package          | Purpose                          |
|------------------|----------------------------------|
| `folium`         | Interactive Leaflet map generator |
| `exifread`       | GPS EXIF metadata extraction     |
| `pandas`         | Data manipulation / CSV output   |
| `opencv-python`  | Image reading and resizing       |
| `numpy`          | Array operations                 |

---

## Notes

- All scripts use **relative paths** — run them from the project root directory.
- The `output/` folder is gitignored; generated files stay local.
- Markers on the map are **colour-coded by location** for easy identification.
