from django.urls import path

from .views import (
    CreateLocationView,
    GetAllLocationsView,
    GetLocationToSelectView,
    UpdateLocationView,
    CancelLocationView,
    PoolView
)

urlpatterns = [
    path('get/', GetAllLocationsView.as_view(), name='get-locations'),
    path('create/', CreateLocationView.as_view(), name='create-location'),
    path('select/', GetLocationToSelectView.as_view(), name='select-location'),
    path('update/<int:pk>/', UpdateLocationView.as_view(), name='update-location'),
    path('cancel/<int:pk>/', CancelLocationView.as_view(), name='cancel-location'),
    path('<int:pk>/pools/', PoolView.as_view(), name='get-pools'),
    path('pool/', PoolView.as_view(), name='pool'),
    path('pool/<int:pk>/', PoolView.as_view(), name='pool-one'),

]
