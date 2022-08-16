from typing import IO, Any
from celery import shared_task
from .models import FileUploadModel
from utils.filter_csv import parse_csv

@shared_task()
def process_csv_file_task(instance_id: int) -> None:
    try:
        instance = FileUploadModel.objects.get(id=instance_id)
    except FileUploadModel.DoesNotExist:
        return None
    instance_path = instance.file.path
    csv_file = parse_csv(instance_path, instance.file.name)
    instance.parse_status = FileUploadModel.COMPLETED
    breakpoint()
    instance.parsed_file = csv_file[0]
    instance.save()
        

def write_file_chunks(file: IO, instance:Any) -> None:
    new_file = file
    file_name = file.name
    with open(file_name, 'wb') as temp_file:
        for chunk in new_file.chunks():
            temp_file.write(chunk)
    instance.file = new_file
    instance.save()
