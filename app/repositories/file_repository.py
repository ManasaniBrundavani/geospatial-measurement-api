from typing import Any


_files: dict[str, dict[str, Any]] = {}


def save_file(
    file_id: str,
    file_data: dict[str, Any]
) -> None:
    """
    Save processed file information.
    """

    _files[file_id] = file_data


def get_file(
    file_id: str
) -> dict[str, Any] | None:
    """
    Retrieve file information by ID.
    """

    return _files.get(file_id)


def delete_file(
    file_id: str
) -> None:
    """
    Delete a file record.
    """

    _files.pop(file_id, None)