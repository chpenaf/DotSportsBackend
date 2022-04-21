from django.contrib import admin

from .models import (
    Catalog, 
    Service, 
    Course,
    Service_Subcategory,
    Course_Level
)

admin.site.register(Catalog)
admin.site.register(Service)
admin.site.register(Course)
admin.site.register(Service_Subcategory)
admin.site.register(Course_Level)