from django.urls import path, include

urlpatterns = [
    path('auth/', include('applications.authentication.api.urls') ),
    path('credits/', include('applications.credits.api.urls') ),
    path('catalog/', include('applications.catalog.api.urls') ),
    path('employees/', include('applications.employees.api.urls') ),
    path('locations/', include('applications.locations.api.urls') ),
    path('main/', include('applications.main.api.urls') ),
    path('members/', include('applications.members.api.urls') ),
    path('planning/', include('applications.planning.api.urls') ),
    path('schedules/', include('applications.schedule.api.urls') ),
    path('users/', include('applications.users.api.urls') ),
]