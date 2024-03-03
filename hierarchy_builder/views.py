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
from hierarchy_builder.services.hierarchy_service import HierarchyService


def index(request):
    return render(request, 'index.html')


class ExcelUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    file_upload = openapi.Parameter('file', in_=openapi.IN_FORM, description="Upload Excel file",
                                    type=openapi.TYPE_FILE, required=True)

    @swagger_auto_schema(manual_parameters=[file_upload],
                         operation_summary="Upload and Process Excel File",
                         responses={201: "Excel file has been processed successfully.",
                                    400: "Invalid file format.",
                                    500: "Internal Server Error"})
    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)

        if serializer.is_valid():
            excel_file = serializer.validated_data['file']
            try:
                with transaction.atomic():
                    excel_service = ExcelService(excel_file)
                    excel_service.process_excel_file()

                return Response({"message": "Excel file has been processed successfully."},
                                status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": f"An error occurred while processing the Excel file: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HierarchyView(APIView):

    @swagger_auto_schema(operation_summary="Get Full Device Hierarchy",
                         operation_description="Retrieves the complete hierarchy of device categories, brands, series, and models from Redis.",
                         responses={200: 'Successfully retrieved the hierarchy',
                                    500: 'Internal Server Error'})
    def get(self, request, *args, **kwargs):
        try:
            hierarchy_data = HierarchyService.get_full_hierarchy()
            return Response(hierarchy_data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
