import geopandas as gpd


def get_measurement_gdf(
    gdf: gpd.GeoDataFrame
) -> tuple[gpd.GeoDataFrame, str]:
    """
    Prepare a GeoDataFrame for accurate measurement.

    Geographic CRS geometries are transformed into an
    appropriate projected CRS before measurements are calculated.

    Returns:
        A measurement-ready GeoDataFrame and the CRS used.
    """

    if gdf.empty:
        raise ValueError(
            "The uploaded file does not contain any features."
        )

    if gdf.crs is None:
        raise ValueError(
            "The uploaded file does not define a CRS."
        )

    # If the source CRS is geographic, such as EPSG:4326,
    # estimate an appropriate local UTM projected CRS.
    if gdf.crs.is_geographic:

        projected_crs = gdf.estimate_utm_crs()

        if projected_crs is None:
            raise ValueError(
                "Unable to determine a suitable projected CRS."
            )

        measurement_gdf = gdf.to_crs(projected_crs)

        return (
            measurement_gdf,
            projected_crs.to_string()
        )

    # If the input is already projected, use it directly.
    return (
        gdf,
        gdf.crs.to_string()
    )