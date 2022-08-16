from django.urls import reverse
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIClient, APITestCase
from django.core.files import File
from unittest import mock
from rest_framework import status
from django.test.utils import override_settings
from csv_processing.models import FileUploadModel
from django.core.files.uploadedfile import SimpleUploadedFile


class CSVProcessingAPITestCase(APITestCase):
    """
    CSV Processing API Test case.
    """

    client = APIClient()

    invalid_file_mock = mock.MagicMock(spec=File, name="FileMock")
    invalid_file_mock.name = "test1.pdf"

    valid_file_mock = mock.MagicMock(spec=File, name="ValidFileMock")
    valid_file_mock.name = "test.csv"

    def test_upload_wrong_file_format(self):
        request_data = {"file": self.invalid_file_mock}
        response = self.client.post(
            reverse("api_csv_upload"),
            request_data,
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Please upload a CSV file.")

    def test_upload_no_file(self):
        request_data = {"file": ""}
        response = self.client.post(
            reverse("api_csv_upload"),
            request_data,
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "Please upload a file.")

    def test_upload_a_csv_file(self):
        request_data = {"file": self.valid_file_mock}
        response = self.client.post(
            reverse("api_csv_upload"),
            request_data,
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that model is created
        instance = FileUploadModel.objects.first()
        self.assertEqual(response.data["processing_id"], instance.processing_id)

        # retrieve the data
        response = self.client.get(
            reverse(
                "api_csv_retrieve", kwargs={"processing_id": instance.processing_id}
            ),
        )
        # file should still be processing since celery isn;t eager
        self.assertEqual(response.data["message"], "File is still being processed.")

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_retrieve_processes_with_real_data(self):
        filename = "test_csv.csv"
        file = File(open("media/testfiles/test_csv.csv", "rb"))
        uploaded_file = SimpleUploadedFile(
            filename, file.read(), content_type="multipart/form-data"
        )
        request_data = {"file": uploaded_file}
        response = self.client.post(
            reverse("api_csv_upload"),
            request_data,
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # assert that model is created
        instance = FileUploadModel.objects.first()
        self.assertEqual(response.data["processing_id"], instance.processing_id)

        # retrieve the data
        response = self.client.get(
            reverse(
                "api_csv_retrieve", kwargs={"processing_id": instance.processing_id}
            ),
        )
        # file should already be processed
        self.assertEqual(
            response.data["processed_file"],
            "http://testserver/media/processed/test_csv_output.csv",
        )
        instance.refresh_from_db()
        # parse status should be completed
        self.assertEqual(instance.parse_status, FileUploadModel.COMPLETED)
