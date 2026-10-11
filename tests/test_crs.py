import geopandas as gpd
from shapely.geometry import Polygon

from app.services.crs_service import (
    get_measurement_gdf,
)


def test_geographic_crs_is_projected():

    polygon = Polygon([
        (78.4800, 17.3800),
        (78.4900, 17.3800),
        (78.4900, 17.3900),
        (78.4800, 17.3900),
        (78.4800, 17.3800),
    ])

    gdf = gpd.GeoDataFrame(
        {
            "name": ["Test Area"]
        },
        geometry=[polygon],
        crs="EPSG:4326",
    )

    measurement_gdf, measurement_crs = (
        get_measurement_gdf(gdf)
    )

    assert measurement_gdf.crs is not None
    assert not measurement_gdf.crs.is_geographic
    assert measurement_crs != "EPSG:4326"