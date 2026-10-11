from fastapi import FastAPI

from app.api.routes.files import router as files_router


app = FastAPI(
    title="Geospatial File Measurement API",
    description=(
        "Backend service for processing KML and Shapefile data "
        "and calculating geospatial measurements."
    ),
    version="1.0.0",
)


app.include_router(files_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }