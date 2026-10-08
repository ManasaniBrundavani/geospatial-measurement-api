from fastapi import FastAPI

app = FastAPI(
    title="Geospatial File Measurement API",
    description=(
        "Backend service for processing KML and Shapefile data "
        "and calculating geospatial measurements."
    ),
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }