from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

from .serializers import CSVFileUploadSerializer

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
            
