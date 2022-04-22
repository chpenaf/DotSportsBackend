from django.urls import path

from .views import (
    CourseAssignedView,
    CourseScheduleView,
    CourseSessionView
)

urlpatterns = [
    path('', CourseAssignedView.as_view(), name='course-assigned'),
    path('location/<int:id_location>/', CourseAssignedView.as_view(), name='course-by-location'),
    path('<int:pk>/', CourseAssignedView.as_view(), name='one-course-assigned'),
    path('schedule/', CourseScheduleView.as_view(), name='course-schedule'),
    path('schedule/<int:pk>/', CourseScheduleView.as_view(), name='one-course-schedule'),
    path('session/', CourseSessionView.as_view(), name='course-session'),
    path('session/<int:pk>/', CourseSessionView.as_view(), name='course-session')
]
