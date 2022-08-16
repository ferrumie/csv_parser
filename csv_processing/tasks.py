from celery import shared_task
from .models import FileUploadModel
from utils.filter_csv import parse_csv

@shared_task()
def process_csv_file_task(filename, instance):
    try:
        csv_file = parse_csv(filename)
        instance.parse_status = FileUploadModel.COMPLETED
        instance.parsed_file = csv_file
        instance.save()
    except FileNotFoundError:
        pass
