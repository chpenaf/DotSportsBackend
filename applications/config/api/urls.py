from django.urls import path

from .views import CapacityPoolView

urlpatterns = [
    path('capacity/pool/', CapacityPoolView.as_view(), name='capacity_pool'),
    path('capacity/pool/<int:pk>/', CapacityPoolView.as_view(), name='capacity_pool_one'),
]
