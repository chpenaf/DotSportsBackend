from django.urls import path, include

urlpatterns = [
    path('auth/', include('applications.authentication.api.urls') ),
    path('members/', include('applications.members.api.urls')),
    path('users/', include('applications.users.api.urls')),
    path('locations/', include('applications.locations.api.urls'))
]