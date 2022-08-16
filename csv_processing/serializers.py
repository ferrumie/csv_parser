import os
from typing import Any, Dict

from rest_framework import serializers

from .models import FileUploadModel

class CSVFileUploadSerializer(serializers.Serializer[Dict[str, Any]]):
    """Serializer for uploading CSV Files."""
    class Meta:

        model = FileUploadModel
        fields = (
            'file',
        )

    def validate_file(self, filename):
        extension = os.path.splitext(filename)[1].replace(".", "")
        if extension.lower() != 'csv':
            raise serializers.ValidationError('Please upload a csv file')
        return filename