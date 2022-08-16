from django.db import models

from .utils import (
    file_download_directory,
    file_upload_directory,
    generate_processing_id,
)

# Create your models here.


class FileUploadModel(models.Model):
    PROCESSING = 0
    COMPLETED = 1
    NOT_STARTED = 2
    PARSE_STATUS = (
        (PROCESSING, "Parse Processing"),
        (COMPLETED, "Parse completed"),
        (NOT_STARTED, "Parse not started"),
    )
    processing_id = models.CharField(
        max_length=32, unique=True, editable=False, default=generate_processing_id
    )
    file = models.FileField(max_length=255, upload_to=file_upload_directory, null=True)
    processed_file = models.FileField(
        max_length=255, upload_to=file_download_directory, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parse_status = models.IntegerField(choices=PARSE_STATUS, default=NOT_STARTED)

    def __str__(self) -> str:
        """
        Unicode representation for File upload model.

        :return: string
        """
        return f"file - {self.processing_id}"
