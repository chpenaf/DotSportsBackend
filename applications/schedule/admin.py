from django.contrib import admin

from .models import Schedule, Schedule_Day, Schedule_Slot

admin.site.register(Schedule)
admin.site.register(Schedule_Day)
admin.site.register(Schedule_Slot)
