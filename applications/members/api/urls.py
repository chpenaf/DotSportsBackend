from django.urls import path

from applications.members.api.views import (
    signup_member,
    ListView,
    CreateView,
    UpdateView,
    RetrieveView,
    CancelView
)

urlpatterns = [
    path('signup/', signup_member, name='sign-up'),
    path('list/', ListView.as_view(), name='list-members'),
    path('create/', CreateView.as_view(), name='create-member'),
    path('get/<int:pk>/', RetrieveView.as_view(), name='get_member'),
    path('update/<int:pk>/', UpdateView.as_view(), name='update-member'),
    path('cancel/<int:pk>/', CancelView.as_view(), name='cancel-member')
]
