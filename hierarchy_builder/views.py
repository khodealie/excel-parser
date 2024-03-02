from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from .serializers import FileUploadSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from hierarchy_builder.services.excel_service import ExcelService

def index(request):
    return render(request, 'index.html')

class ExcelUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    file_upload = openapi.Parameter('file', in_=openapi.IN_FORM, description="Upload Excel file",
                                    type=openapi.TYPE_FILE, required=True)

    @swagger_auto_schema(manual_parameters=[file_upload])
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            excel_file = serializer.validated_data['file']
            try:
                with transaction.atomic():
                    excel_service = ExcelService(excel_file)
                    excel_service.process_excel_file()

                return Response({"message": "Excel file has been processed successfully."}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"An error occurred while processing the Excel file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
