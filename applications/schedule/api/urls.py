from django.urls import path

from .views import ( 
    ListView, 
    RetrieveView,
    ScheduleView,
    ScheduleAPIView,
    ScheduleDayApiView,
    ScheduleSlotApiView,
    getDayTypes
)

urlpatterns = [
    path('get/daytypes/', getDayTypes, name='get-daytypes'),
    path('get/location/<int:id>/', ListView.as_view(), name='list-schedules'),
    path('get/<int:pk>/', RetrieveView.as_view(), name='get-location-schedule'),
    path('save/', ScheduleView.as_view(), name='save-schedule'),
    path('save/<int:pk>/', ScheduleAPIView.as_view(), name='update-schedule'),
    path('day/', ScheduleDayApiView.as_view(), name='create-schedule-day'),
    path('day/slots/', ScheduleSlotApiView.as_view(), name='create-schedule-slot'),
]