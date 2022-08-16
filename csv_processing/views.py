from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from django.shortcuts import get_object_or_404

from rest_framework.generics import ListAPIView
from .tasks import process_csv_file_task

from csv_processing.serializers import CSVFileListSerializer, CSVFileRetrieveSerializer, CSVFileUploadSerializer
from csv_processing.models import FileUploadModel

class CSVFileUploadView(APIView):
    serializer_class = CSVFileUploadSerializer
    parser_classes = [FileUploadParser]

    def post(self, request: Request, *args: dict, **kwargs: dict) -> Response:
        """Receives uploaded CSV file."""
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)   

        # run a celery task to process the file
        # save the file in the model
        file = serializer.validated_data['file']
        instance = serializer.save(commit=False)
        instance.parse_status = FileUploadModel.PROCESSING
        instance.save()
        process_csv_file_task.delay(file, instance)

        # return the processing id
        response = {
            "processing_id": instance.processing_id
        }
        return Response(response, status=status.HTTP_200_OK)


class CSVFileRetrieveView(APIView):
    serializer_class = CSVFileRetrieveSerializer

    def get(self, request: Request, *args: dict, **kwargs: dict) -> Response:
        """Returns the processed CSV file if ready."""
        processing_id = self.kwargs.get('id')
        instance = get_object_or_404(FileUploadModel, processing_id=processing_id)
        if instance.parse_status != FileUploadModel.COMPLETED:
            return Response({"message": "File is still being processed."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CSVListView(ListAPIView):
    serializer_class = CSVFileListSerializer
    queryset = FileUploadModel
