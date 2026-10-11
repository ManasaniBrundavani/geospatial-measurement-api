
from pathlib import Path
import zipfile
import geopandas as gpd
from shapely.geometry import Polygon

base = Path("sample_data/generated_shapefile")
base.mkdir(parents=True, exist_ok=True)

gdf = gpd.GeoDataFrame(
    {"name": ["Test Polygon"]},
    geometry=[
        Polygon([
            (78.0, 17.0),
            (78.01, 17.0),
            (78.01, 17.01),
            (78.0, 17.01),
            (78.0, 17.0),
        ])
    ],
    crs="EPSG:4326",
)

shapefile_path = base / "sample.shp"
gdf.to_file(shapefile_path)

zip_path = Path("sample_data/valid_shapefile.zip")

with zipfile.ZipFile(
    zip_path, "w", compression=zipfile.ZIP_DEFLATED
) as archive:
    for path in base.iterdir():
        if path.is_file():
            archive.write(path, arcname=path.name)

print("Created:", zip_path.resolve())
print("Is valid ZIP:", zipfile.is_zipfile(zip_path))

with zipfile.ZipFile(zip_path, "r") as archive:
    print("Files:", archive.namelist())
    print("Integrity check:", archive.testzip())
