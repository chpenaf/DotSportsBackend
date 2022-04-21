from django.urls import path

from .views import ( 
    CatalogView,
    ServiceView 
)

urlpatterns = [
    path('', CatalogView.as_view(), name='catalogs'),
    path('<int:id_location>/', CatalogView.as_view(), name='catalog'),
    path('services/', ServiceView.as_view(), name='services'),
    path('services/<int:pk>/', ServiceView.as_view(), name='service')
]
