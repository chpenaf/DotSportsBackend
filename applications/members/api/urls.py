from django.urls import path

from .views import signup_member

urlpatterns = [
    path('signup/', signup_member, name='sign-up'),
]
