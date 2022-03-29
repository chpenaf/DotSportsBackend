from django.urls import path

from .views import (
    CreateLocationView,
    GetAllLocationsView
)

urlpatterns = [
    path('create/', CreateLocationView.as_view(), name='create-location'),
    path('get/', GetAllLocationsView.as_view(), name='get-locations'),
]
