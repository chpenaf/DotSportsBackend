
from django.urls import path

from applications.employees.api.views import (
    ListEmployeesView,
    CreateEmployeeView,
    UpdateEmployeeView,
    RetrieveEmployee,
    RetrieveLogged,
    CancelEmployee
)

urlpatterns = [
    path('list/', ListEmployeesView.as_view(), name='list-employees'),
    path('create/', CreateEmployeeView.as_view(), name='create-employee'),
    path('update/<int:pk>/', UpdateEmployeeView.as_view(), name='update-employee'),
    path('get/<int:pk>/', RetrieveEmployee.as_view(), name='get-employee'),
    path('get/logged/', RetrieveLogged.as_view(), name='get-logged-employee'),
    path('cancel/<int:pk>/', CancelEmployee.as_view(), name='cancel-employee'),
]
