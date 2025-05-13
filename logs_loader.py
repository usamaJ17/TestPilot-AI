from pathlib import Path


def ensure_logs_file(filename: str = "fastagent.jsonl") -> Path:
    """
    Ensure that a logs file exists in the project root directory.
    If not present, create an empty file.

    Args:
        filename (str): Name of the logs file.

    Returns:
        Path: Path object pointing to the logs file.
    """
    root_dir = Path(__file__).resolve().parent
    file_path = root_dir / filename

    if not file_path.exists():
        file_path.touch()

    return file_path
