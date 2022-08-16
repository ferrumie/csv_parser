from celery import shared_task
from utils.filter_csv import parse_csv

@shared_task()
def process_csv_file_task(filename):
    csv_file = parse_csv(filename)
    