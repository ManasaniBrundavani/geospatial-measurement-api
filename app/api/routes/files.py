from fastapi import APIRouter, File, HTTPException, UploadFile

from app.repositories.file_repository import (
    get_file,
    save_file,
)

from app.services.crs_service import (
    get_measurement_gdf,
)

from app.services.file_service import (
    generate_file_id,
    read_geospatial_file,
)

from app.services.geospatial_service import (
    extract_features,
)

from app.services.measurement_service import (
    calculate_feature_measurements,
)

from app.utils.file_validation import validate_file


router = APIRouter(
    prefix="/api/files",
    tags=["Files"],
)



@router.post("/")
async def upload_file(
    file: UploadFile = File(...)
):
    """
    Upload and process a KML file or a ZIP
    containing a Shapefile.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    file_bytes = await file.read()

    try:
        # Validate extension, empty content, and file size.
        validate_file(
            file.filename,
            file_bytes
        )

        # Continue with your existing processing logic.
        gdf = read_geospatial_file(
            file_bytes,
            file.filename
        )

        features = extract_features(gdf)

        measurement_gdf, measurement_crs = (
            get_measurement_gdf(gdf)
        )

        measurements = calculate_feature_measurements(
            measurement_gdf
        )

        file_id = generate_file_id()

        source_crs = (
            gdf.crs.to_string()
            if gdf.crs
            else None
        )

        file_data = {
            "id": file_id,
            "filename": file.filename,
            "feature_count": len(gdf),
            "crs": source_crs,
            "measurement_crs": measurement_crs,
            "status": "COMPLETED",
            "features": features,
            "measurements": measurements,
        }

        save_file(file_id, file_data)

        return {
            "id": file_id,
            "filename": file.filename,
            "feature_count": len(gdf),
            "crs": source_crs,
            "status": "COMPLETED",
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        ) from exc

    
@router.get("/{file_id}")
def get_file_information(
    file_id: str
):
    """
    Return information about an uploaded file.
    """

    file_data = get_file(file_id)

    if file_data is None:
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    return {
        "id": file_data["id"],
        "filename": file_data["filename"],
        "feature_count": file_data["feature_count"],
        "crs": file_data["crs"],
        "status": file_data["status"],
    }


@router.get("/{file_id}/measurements")
def get_file_measurements(
    file_id: str
):
    """
    Return measurements for all features
    in the uploaded file.
    """

    file_data = get_file(file_id)

    if file_data is None:
        raise HTTPException(
            status_code=404,
            detail="File not found."
        )

    return {
        "file_id": file_data["id"],
        "measurements": file_data["measurements"],
    }