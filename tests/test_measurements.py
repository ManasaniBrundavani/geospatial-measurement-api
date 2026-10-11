from shapely.geometry import (
    LineString,
    Point,
    Polygon,
)

from app.services.measurement_service import (
    calculate_measurement,
)


def test_polygon_measurement():
    polygon = Polygon([
        (0, 0),
        (10, 0),
        (10, 10),
        (0, 10),
        (0, 0),
    ])

    result = calculate_measurement(polygon)

    assert result is not None
    assert result["type"] == "area"
    assert result["value"] == 100.0
    assert result["unit"] == "square_meters"


def test_linestring_measurement():
    line = LineString([
        (0, 0),
        (3, 4),
    ])

    result = calculate_measurement(line)

    assert result is not None
    assert result["type"] == "length"
    assert result["value"] == 5.0
    assert result["unit"] == "meters"


def test_point_has_no_measurement():
    point = Point(10, 20)

    result = calculate_measurement(point)

    assert result is None