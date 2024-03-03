from django.contrib import admin
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from hierarchy_builder.views import ExcelUploadView, HierarchyView, index  # Make sure to import HierarchyView

# Swagger schema view setup
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Detailed API documentation for the project",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Django index URL
    path('', index, name='index'),

    # Django admin URL
    path('admin/', admin.site.urls),

    # Your custom file upload URL
    path('upload/', ExcelUploadView.as_view(), name='excel-upload'),

    # URL for HierarchyView
    path('hierarchy/', HierarchyView.as_view(), name='device-hierarchy'),  # Add this line

    # Swagger Documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
