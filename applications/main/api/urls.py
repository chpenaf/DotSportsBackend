from django.urls import path

from applications.main.api.views import (
    #get_now,
    GetApps,
    ApplicationAPIView
    )

urlpatterns = [
    #path('now/', get_now, name='today'),
    path('apps/', GetApps.as_view(), name='apps'),
    path('apps/update/', ApplicationAPIView.as_view(), name='save-apps'),
    path('apps/delete/<int:pk>/', ApplicationAPIView.as_view(), name='delete-app')
]