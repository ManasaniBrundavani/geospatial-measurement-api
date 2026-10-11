from typing import Any

import geopandas as gpd


SUPPORTED_GEOMETRIES = {
    "Polygon",
    "MultiPolygon",
    "LineString",
    "MultiLineString",
    "Point",
    "MultiPoint",
}


def calculate_measurement(
    geometry: Any
) -> dict[str, Any] | None:
    """
    Calculate a measurement for a geometry.

    Polygon / MultiPolygon:
        Area in square meters.

    LineString / MultiLineString:
        Length in meters.

    Point / MultiPoint:
        No measurement required.

    Unsupported geometry:
        Returns None.
    """

    if geometry is None:
        return None

    geometry_type = geometry.geom_type

    if geometry_type in {"Polygon", "MultiPolygon"}:

        return {
            "type": "area",
            "value": round(float(geometry.area), 2),
            "unit": "square_meters",
        }

    if geometry_type in {
        "LineString",
        "MultiLineString",
    }:

        return {
            "type": "length",
            "value": round(float(geometry.length), 2),
            "unit": "meters",
        }

    if geometry_type in {
        "Point",
        "MultiPoint",
    }:

        return None

    return None


def calculate_feature_measurements(
    measurement_gdf: gpd.GeoDataFrame,
) -> list[dict[str, Any]]:

    measurements = []

    for index, row in measurement_gdf.iterrows():

        geometry = row.geometry

        measurement = calculate_measurement(
            geometry
        )

        measurements.append(
            {
                "feature_id": index,
                "geometry_type": (
                    geometry.geom_type
                    if geometry is not None
                    else None
                ),
                "measurement": measurement,
            }
        )

    return measurements