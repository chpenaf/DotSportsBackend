from django.urls import path

from .views import (
    CourseAssignedView,
    CourseScheduleView,
    CourseSessionView,
    get_schedule_week
)

urlpatterns = [
    path('', CourseAssignedView.as_view(), name='course-assigned'),
    path('location/<int:id_location>/', CourseAssignedView.as_view(), name='course-by-location'),
    path('<int:pk>/', CourseAssignedView.as_view(), name='one-course-assigned'),
    path('schedule/', CourseScheduleView.as_view(), name='course-schedule'),
    path('schedule/<int:pk>/', CourseScheduleView.as_view(), name='one-course-schedule'),
    path('schedule/week/<int:pk>/', get_schedule_week, name='course-schedule'),
    path('session/', CourseSessionView.as_view(), name='course-session'),
    path('session/<int:year>/<int:month>/<int:day>/', CourseSessionView.as_view(), name='course-session-date'),
    path('session/<int:pk>/', CourseSessionView.as_view(), name='course-session')
]
