from django.db import models
from hierarchy_builder.models.series import Series

class DeviceModel(models.Model):
    name = models.CharField(max_length=255)
    series = models.ForeignKey(Series, on_delete=models.CASCADE, related_name='device_models')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
