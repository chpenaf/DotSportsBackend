from django.urls import path

from .views import currentUser

urlpatterns = [
    path('current/', currentUser, name='current_user') 
]
 