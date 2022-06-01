from django.urls import path

from .views import ( 
    CatalogView,
    CourseView,
    LevelView,
    ServiceView,
    SubcategoryView
)

urlpatterns = [
    path('', CatalogView.as_view(), name='catalogs'),
    path('<int:id_location>/', CatalogView.as_view(), name='catalog'),
    path('services/', ServiceView.as_view(), name='services'),
    path('services/<int:pk>/', ServiceView.as_view(), name='service'),
    path('subcategory/<int:pk>/', SubcategoryView.as_view(), name='subcategory'),
    path('courses/', CourseView.as_view(), name='courses'),
    path('courses/id/<int:pk>/', CourseView.as_view(), name='course-one'),
    path('courses/<int:id_location>/', CourseView.as_view(), name='course'),
    path('courses/levels/', LevelView.as_view(), name='levels'),
    path('courses/levels/<int:pk>/', LevelView.as_view(), name='level')
]
