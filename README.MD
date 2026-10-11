# Geospatial File Measurement API

A REST API built with FastAPI and GeoPandas to upload, process, and measure geospatial data from KML files and ZIP archives containing Shapefiles.

## Features

- Upload KML files and Shapefile ZIP archives.
- Extract feature IDs, geometry types, geometries, CRS information, and feature properties.
- Calculate polygon areas and line lengths.
- Return no measurement for point geometries.
- Reproject geographic coordinates before calculating measurements.
- Validate file extensions, empty uploads, ZIP integrity, Shapefile components, and unsafe archive paths.
- Retrieve uploaded file information and feature measurements through REST endpoints.
- Automated tests using pytest.

## Technology Stack

- **Python 3.10+**
- **FastAPI** — REST API framework
- **GeoPandas** — geospatial file processing
- **Shapely** — geometry operations
- **PyProj** — coordinate reference system transformations
- **Pytest** — automated testing

## Project Structure

```text
geospatial-measurement-api/
├── app/
│   ├── api/routes/
│   ├── repositories/
│   ├── services/
│   ├── utils/
│   └── main.py
├── tests/
│   ├── test_api.py
│   ├── test_crs.py
│   ├── test_measurements.py
│   └── test_zip_validation.py
├── sample_data/
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup and Installation

### 1. Clone the repository

```bash
git clone YOUR_PUBLIC_GITHUB_REPOSITORY_URL
cd geospatial-measurement-api
```

Replace the URL above with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- API base URL: `http://127.0.0.1:8000`
- Interactive Swagger documentation: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`

## API Endpoints

### 1. Upload a geospatial file

`POST /api/files/`

Accepts a `.kml` file or a `.zip` archive containing one Shapefile.

Example success response:

```json
{
  "id": "generated-file-id",
  "filename": "sample.kml",
  "feature_count": 3,
  "crs": "EPSG:4326",
  "status": "COMPLETED"
}
```

### 2. Retrieve file information

`GET /api/files/{file_id}`

Returns the uploaded file's ID, filename, feature count, source CRS, and processing status.

### 3. Retrieve feature measurements

`GET /api/files/{file_id}/measurements`

Returns the calculated measurements for the uploaded file.

### 4. Health check

`GET /health`

Returns the API health status.

## Measurement Strategy

| Geometry type | Measurement | Unit |
|---|---|---|
| Polygon | Area | Square meters |
| MultiPolygon | Area | Square meters |
| LineString | Length | Meters |
| MultiLineString | Length | Meters |
| Point | No measurement | Not applicable |
| MultiPoint | No measurement | Not applicable |

Unsupported geometry types do not receive a measurement.

## Coordinate Reference System (CRS) Handling

Area and length calculations must not be performed directly on longitude and latitude coordinates.

When the source CRS is geographic, the API estimates a suitable UTM projected CRS and transforms the geometry before calculating measurements. The source CRS is retained in the file information, and the measurement CRS is stored separately.

Files without CRS information are rejected because the API cannot reliably interpret their coordinates.

The current UTM estimation strategy is best suited to datasets that fit within a suitable UTM zone. Very large datasets or geometries spanning multiple zones may require a different projection strategy.

## File Validation and Security

- Only `.kml` and `.zip` extensions are accepted.
- Uploaded files are limited to 10 MB.
- Extracted ZIP contents are limited to 50 MB.
- ZIP path traversal and symbolic links are rejected.
- ZIP integrity is checked before extraction.
- Exactly one Shapefile is expected in a ZIP archive.
- Required Shapefile components are checked before processing.
- Invalid inputs return descriptive HTTP errors.

## Running Tests

Run the complete automated test suite:

```bash
pytest -v
```

The test suite covers API behavior, geometry measurements, CRS transformations, invalid uploads, and ZIP validation.

## Architecture and Processing Flow

1. The client uploads a KML file or Shapefile ZIP.
2. The API validates the filename, extension, and file contents.
3. The file service reads the geospatial data.
4. The geospatial service extracts feature information and properties.
5. The CRS service prepares projected geometries for measurements.
6. The measurement service calculates area or length based on geometry type.
7. The repository stores the processed result in memory.
8. The API returns a file ID that can be used to retrieve information and measurements.

## Design Decisions and Limitations

- FastAPI provides request handling and interactive API documentation.
- GeoPandas and PyProj simplify geospatial processing and CRS transformations.
- The current repository uses in-memory storage, so uploaded file records are lost when the application restarts.
- The API currently processes files synchronously.
- Authentication and persistent database storage are not implemented.
- Measurement accuracy depends on the suitability of the selected projected CRS.

## Learning Outcomes

This project provided practical experience with REST API development, geospatial file processing, coordinate transformations, geometry measurements, input validation, secure archive extraction, and automated testing.

## Future Scope

- Persistent storage using PostgreSQL with PostGIS.
- Asynchronous processing for large datasets.
- Authentication and authorization.
- More advanced CRS selection for large or multi-zone datasets.
- Docker-based deployment and continuous integration.
- Structured logging, monitoring, and improved operational observability.
