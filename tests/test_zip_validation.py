
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from app.services.file_service import (
    _find_shapefile,
    _safe_extract_zip,
)


def test_corrupted_zip_is_rejected():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        zip_path = root / "invalid.zip"
        extract_dir = root / "extracted"
        extract_dir.mkdir()

        zip_path.write_bytes(b"This is not a ZIP archive.")

        with pytest.raises(ValueError, match="Invalid or corrupted ZIP"):
            _safe_extract_zip(zip_path, extract_dir)


def test_zip_without_shapefile_is_rejected():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        zip_path = root / "no_shapefile.zip"
        extract_dir = root / "extracted"
        extract_dir.mkdir()

        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.writestr("readme.txt", "No Shapefile here.")

        _safe_extract_zip(zip_path, extract_dir)

        with pytest.raises(ValueError, match="does not contain a Shapefile"):
            _find_shapefile(extract_dir)


def test_shapefile_missing_prj_is_rejected():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        extract_dir = root / "extracted"
        extract_dir.mkdir()

        for extension in (".shp", ".shx", ".dbf"):
            (extract_dir / f"sample{extension}").write_bytes(b"test")

        with pytest.raises(ValueError, match="missing required components"):
            _find_shapefile(extract_dir)


def test_multiple_shapefiles_are_rejected():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        extract_dir = root / "extracted"
        extract_dir.mkdir()

        for name in ("first", "second"):
            for extension in (".shp", ".shx", ".dbf", ".prj"):
                (extract_dir / f"{name}{extension}").write_bytes(b"test")

        with pytest.raises(ValueError, match="multiple Shapefiles"):
            _find_shapefile(extract_dir)


def test_zip_path_traversal_is_rejected():
    with TemporaryDirectory() as temp:
        root = Path(temp)
        zip_path = root / "unsafe.zip"
        extract_dir = root / "extracted"
        extract_dir.mkdir()

        with zipfile.ZipFile(zip_path, "w") as archive:
            archive.writestr("../outside.txt", "unsafe")

        with pytest.raises(ValueError, match="Unsafe ZIP archive"):
            _safe_extract_zip(zip_path, extract_dir)
