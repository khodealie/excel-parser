from rest_framework import serializers

# Serializer for handling file uploads
class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)
