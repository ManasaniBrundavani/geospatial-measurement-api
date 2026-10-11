from typing import Any
import math

import geopandas as gpd
from shapely.geometry import mapping


def make_json_safe(value: Any) -> Any:
    """
    Convert values that are not valid JSON into JSON-safe values.

    In particular, NaN and infinite floating-point values are
    converted to None.
    """

    if value is None:
        return None

    if isinstance(value, float):
        if not math.isfinite(value):
            return None

        return value

    if hasattr(value, "item"):
        try:
            value = value.item()
        except (ValueError, TypeError):
            pass

    if isinstance(value, float):
        if not math.isfinite(value):
            return None

    return value


def extract_features(
    gdf: gpd.GeoDataFrame
) -> list[dict[str, Any]]:
    """
    Convert GeoDataFrame features into JSON-serializable dictionaries.
    """

    features = []

    crs_name = (
        gdf.crs.to_string()
        if gdf.crs
        else None
    )

    for index, row in gdf.iterrows():

        geometry = row.geometry

        properties = {}

        for column in gdf.columns:

            if column == "geometry":
                continue

            value = row[column]

            value = make_json_safe(value)

            properties[column] = value

        feature = {
            "feature_id": make_json_safe(index),
            "geometry_type": (
                geometry.geom_type
                if geometry is not None
                else None
            ),
            "geometry": (
                mapping(geometry)
                if geometry is not None
                else None
            ),
            "crs": crs_name,
            "properties": properties,
        }

        features.append(feature)

    return features