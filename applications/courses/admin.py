from django.contrib import admin

from .models import (
    CourseAssigned,
    CourseSchedule,
    CourseSession
)

admin.site.register(CourseAssigned)
admin.site.register(CourseSchedule)
admin.site.register(CourseSession)