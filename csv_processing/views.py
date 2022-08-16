from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser
from django.shortcuts import get_object_or_404

import os

from rest_framework.generics import ListAPIView

from .tasks import process_csv_file_task, write_file_chunks

from csv_processing.serializers import CSVFileListSerializer, CSVFileRetrieveSerializer, CSVFileUploadSerializer
from csv_processing.models import FileUploadModel

class CSVFileUploadView(APIView):
    serializer_class = CSVFileUploadSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request: Request, *args: dict, **kwargs: dict) -> Response:
        """Receives uploaded CSV file."""

        # run a celery task to process the file
        # save the file in the model
        file = request.FILES.get('file')
        if file:
            if not file.name.lower().endswith('csv'):
                return Response({"message": "Please upload a CSV file."}, status=status.HTTP_200_OK)

            # write file chunks into a proper file
            instance = FileUploadModel.objects.create(parse_status = FileUploadModel.PROCESSING)
            write_file_chunks(file, instance)

            # process and save the celery file
            process_csv_file_task(instance.id)

            # return the processing id
            response = {
                "processing_id": str(instance.processing_id)
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({"message": "Please upload a file."}, status=status.HTTP_200_OK)


class CSVFileRetrieveView(APIView):
    serializer_class = CSVFileRetrieveSerializer
    parser_classes = (JSONParser,)
    queryset = FileUploadModel.objects.all()

    def get(self, request: Request, *args: dict, **kwargs: dict) -> Response:
        """Returns the processed CSV file if ready."""
        processing_id = self.kwargs.get('processing_id')
        instance = get_object_or_404(FileUploadModel, processing_id=processing_id)
        if instance.parse_status != FileUploadModel.COMPLETED:
            return Response({"message": "File is still being processed."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance)
        response = {
            'parsed_file': instance.parsed_file.path
        }
        return Response(response, status=status.HTTP_200_OK)

class CSVListView(ListAPIView):
    parser_classes = (MultiPartParser,)
    serializer_class = CSVFileListSerializer
    queryset = FileUploadModel.objects.all()
