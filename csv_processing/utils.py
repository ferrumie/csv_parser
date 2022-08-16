
import uuid
from typing import Any


def file_upload_directory(instance: Any, filename: str) -> str:
    return f'uploads/{str(instance.processing_id)[:-5]}/{filename}/'

def generate_processing_id() -> str:
    uuid.uuid4().hex