from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CSVFileUploadSerializer

class CSVFileUploadView(APIView):
    serializer_class = CSVFileUploadSerializer

    def post(self, request: Request, *args: dict, **kwargs: dict) -> Response:
        """Receives uploaded CSV file."""
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
