from django.urls import path

from .views import BookingView, get_next_booking, get_booking_slot

urlpatterns = [
    path('', BookingView.as_view(), name='booking'),
    path('<int:pk>/', BookingView.as_view(), name='booking-pk'),
    path('member/<int:id_member>/', BookingView.as_view(), name='booking-member'),
    path('member/next/', get_next_booking, name='next-book-member'),
    path('slot/<int:pk>/', get_booking_slot, name='slot-members')
]
