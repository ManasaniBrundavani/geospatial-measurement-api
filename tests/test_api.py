
from fastapi.testclient import TestClient

from app.main import app
from app.repositories.file_repository import delete_file

client = TestClient(app)


def upload_test_kml():
    kml_content = b"""<?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
      <Document>
        <Placemark>
          <name>Test Point</name>
          <Point>
            <coordinates>78.0,17.0</coordinates>
          </Point>
        </Placemark>
      </Document>
    </kml>
    """

    return client.post(
        "/api/files/",
        files={
            "file": (
                "test.kml",
                kml_content,
                "application/vnd.google-earth.kml+xml",
            )
        },
    )


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_upload_kml():
    response = upload_test_kml()

    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.kml"
    assert data["feature_count"] == 1
    assert data["status"] == "COMPLETED"

    delete_file(data["id"])


def test_get_file_information():
    upload_response = upload_test_kml()
    assert upload_response.status_code == 200

    file_id = upload_response.json()["id"]

    try:
        response = client.get(f"/api/files/{file_id}")

        assert response.status_code == 200
        assert response.json()["id"] == file_id
        assert response.json()["feature_count"] == 1
    finally:
        delete_file(file_id)


def test_get_file_measurements():
    upload_response = upload_test_kml()
    assert upload_response.status_code == 200

    file_id = upload_response.json()["id"]

    try:
        response = client.get(
            f"/api/files/{file_id}/measurements"
        )

        assert response.status_code == 200
        assert response.json()["file_id"] == file_id
        assert len(response.json()["measurements"]) == 1
    finally:
        delete_file(file_id)


def test_unsupported_file_extension():
    response = client.post(
        "/api/files/",
        files={
            "file": (
                "notes.txt",
                b"not a geospatial file",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400


def test_empty_file():
    response = client.post(
        "/api/files/",
        files={
            "file": (
                "empty.kml",
                b"",
                "application/vnd.google-earth.kml+xml",
            )
        },
    )

    assert response.status_code == 400


def test_nonexistent_file():
    response = client.get(
        "/api/files/nonexistent-file-id"
    )

    assert response.status_code == 404
