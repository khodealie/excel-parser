from django.db import models
from hierarchy_builder.models.device_category import DeviceCategory

class Brand(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(DeviceCategory, on_delete=models.CASCADE, related_name='brands')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
