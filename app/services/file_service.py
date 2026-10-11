import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from uuid import uuid4

import geopandas as gpd


def generate_file_id() -> str:
    """
    Generate a unique identifier for an uploaded file.
    """
    return str(uuid4())



from pathlib import Path, PurePosixPath
import zipfile


MAX_UNCOMPRESSED_SIZE = 50 * 1024 * 1024  # 50 MB


def _safe_extract_zip(
    zip_path: Path,
    extract_directory: Path,
) -> None:
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            members = zip_ref.infolist()

            total_size = sum(member.file_size for member in members)

            if total_size > MAX_UNCOMPRESSED_SIZE:
                raise ValueError(
                    "ZIP archive exceeds the 50 MB extracted-size limit."
                )

            for member in members:
                # Normalize separators to check Windows and ZIP paths safely.
                normalized_name = member.filename.replace("\\", "/")
                archive_path = PurePosixPath(normalized_name)

                if (
                    archive_path.is_absolute()
                    or ".." in archive_path.parts
                    or ":" in normalized_name
                ):
                    raise ValueError(
                        "Unsafe ZIP archive: invalid file path."
                    )

                # Reject symbolic links in the archive.
                unix_mode = member.external_attr >> 16
                if unix_mode & 0o170000 == 0o120000:
                    raise ValueError(
                        "Unsafe ZIP archive: symbolic links are not allowed."
                    )

                target_path = (
                    extract_directory / normalized_name
                ).resolve()

                if not target_path.is_relative_to(
                    extract_directory.resolve()
                ):
                    raise ValueError(
                        "Unsafe ZIP archive: path traversal detected."
                    )

            # Test archive integrity before extracting.
            if zip_ref.testzip() is not None:
                raise ValueError(
                    "ZIP archive is corrupted."
                )

            zip_ref.extractall(extract_directory)

    except zipfile.BadZipFile as exc:
        raise ValueError(
            "Invalid or corrupted ZIP archive."
        ) from exc


def _find_shapefile(directory: Path) -> Path:
    shapefiles = [
        path
        for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() == ".shp"
    ]

    if not shapefiles:
        raise ValueError(
            "ZIP archive does not contain a Shapefile (.shp)."
        )

    if len(shapefiles) > 1:
        raise ValueError(
            "ZIP archive contains multiple Shapefiles. "
            "Please provide a ZIP containing one Shapefile."
        )

    shapefile = shapefiles[0]
    component_extensions = {
        path.suffix.lower()
        for path in shapefile.parent.iterdir()
        if path.is_file()
        and path.stem.lower() == shapefile.stem.lower()
    }

    required_extensions = {".shp", ".shx", ".dbf", ".prj"}
    missing_extensions = required_extensions - component_extensions

    if missing_extensions:
        missing = ", ".join(sorted(missing_extensions))
        raise ValueError(
            f"Shapefile is missing required components: {missing}."
        )

    return shapefile



def read_geospatial_file(
    file_bytes: bytes,
    filename: str
) -> gpd.GeoDataFrame:

    extension = Path(filename).suffix.lower()

    with tempfile.TemporaryDirectory() as temp_dir:

        temp_path = Path(temp_dir)

        uploaded_file = temp_path / Path(filename).name
        uploaded_file.write_bytes(file_bytes)

        if extension == ".kml":

            gdf = gpd.read_file(
                uploaded_file,
                driver="KML"
            )

        elif extension == ".zip":

            extract_directory = temp_path / "extracted"
            extract_directory.mkdir()

            _safe_extract_zip(
                uploaded_file,
                extract_directory
            )

            shapefile_path = _find_shapefile(
                extract_directory
            )

            gdf = gpd.read_file(
                shapefile_path
            )

        else:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        return gdf