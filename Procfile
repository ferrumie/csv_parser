release: python manage.py migrate --no-input
web: gunicorn csv_parser.wsgi --log-file -
worker: celery -A csv_parser worker --beat