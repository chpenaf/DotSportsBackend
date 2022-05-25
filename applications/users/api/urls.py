from django.urls import path

from .views import currentUser, PasswordView

urlpatterns = [
    path('current/', currentUser, name='current_user'),
    path('current/change-password/', PasswordView.as_view(), name='change-password')
]
 