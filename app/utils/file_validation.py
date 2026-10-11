
from pathlib import Path

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".kml", ".zip"}


def validate_file_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{extension}'. "
            "Allowed types are .kml and .zip."
        )

    return extension


def validate_file(filename: str, file_bytes: bytes) -> str:
    if not filename or not filename.strip():
        raise ValueError("A filename is required.")

    extension = validate_file_extension(filename)

    if not file_bytes:
        raise ValueError("The uploaded file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise ValueError("File size exceeds the 10 MB limit.")

    return extension
