from django.urls import path

from .views import ( 
    CatalogView,
    CourseView,
    ServiceView,
    SubcategoryView
)

urlpatterns = [
    path('', CatalogView.as_view(), name='catalogs'),
    path('<int:id_location>/', CatalogView.as_view(), name='catalog'),
    path('services/', ServiceView.as_view(), name='services'),
    path('services/<int:pk>/', ServiceView.as_view(), name='service'),
    path('subcategory/<int:pk>/', SubcategoryView.as_view(), name='subcategory'),
    path('courses/', CourseView.as_view(), name='course')
]
