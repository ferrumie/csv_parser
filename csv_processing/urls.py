from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from csv_processing.views import CSVFileRetrieveView, CSVFileUploadView, CSVListView

schema_view = get_schema_view(
    openapi.Info(
        title="CSV Processor API",
        default_version="V1",
        description="Api For Availability Check",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(
        "upload/",CSVFileUploadView.as_view(),name="api_csv_upload",
    ),
    path(
        "file/<slug:processing_id>/",CSVFileRetrieveView.as_view(),name="api_csv_retrieve",
    ),
    path(
        "files/",CSVListView.as_view(),name="api_csv_list",
    ),
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]