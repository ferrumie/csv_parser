import uuid
from typing import IO, Any


def file_upload_directory(instance: Any, filename: str) -> str:
    return f"uploads/{str(instance.processing_id)[:-25]}/{filename}"


def file_download_directory(instance: Any, filename: str) -> str:
    return f"download/{filename}"


def generate_processing_id() -> str:
    return uuid.uuid4().hex
