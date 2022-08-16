from django.urls import path

from .views import CSVFileRetrieveView, CSVFileUploadView, CSVListView

urlpatterns = [
    path(
        "upload/",CSVFileUploadView.as_view(),name="api_csv_upload",
    ),
    path(
        "file/<slug:processing_id>/",CSVFileRetrieveView.as_view(),name="api_csv_retrieve",
    ),
    path(
        "files/",CSVListView.as_view(),name="api_csv_list",
    )
]