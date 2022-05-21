from django.urls import path

from .views import BookingView

urlpatterns = [
    path('', BookingView.as_view(), name='booking'),
    path('<int:pk>/', BookingView.as_view(), name='booking-pk'),
    path('member/<int:id_member>/', BookingView.as_view(), name='booking-member'),
]
