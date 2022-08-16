from typing import IO, Any
from celery import shared_task
from csv_processing.models import FileUploadModel
from utils.filter_csv import parse_csv
import os


@shared_task()
def process_csv_file_task(instance_id: int) -> None:
    try:
        instance = FileUploadModel.objects.get(id=instance_id)
    except FileUploadModel.DoesNotExist:
        return None
    instance_path = instance.file.path
    csv_file = parse_csv(instance_path, instance.file.name)
    instance.parse_status = FileUploadModel.COMPLETED

    # get the relative part by splitting the path returned by dask
    rel_path = ("/").join(csv_file[0].split("/")[-2:])
    instance.processed_file = rel_path
    instance.save()
