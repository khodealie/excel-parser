from django.contrib import admin
from .models import DeviceCategory, Brand, Series, DeviceModel

admin.site.register(DeviceCategory)
admin.site.register(Brand)
admin.site.register(Series)
admin.site.register(DeviceModel)
