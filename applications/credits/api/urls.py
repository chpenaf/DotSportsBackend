from django.urls import path

from .views import CreditView, get_quant_credits

urlpatterns = [
    path('credit/', CreditView.as_view(), name='credit' ),
    path('credit/<int:id_member>/', CreditView.as_view(), name='credit-member'),
    path('credit/<int:id_member>/quant/', get_quant_credits, name='credits-by-member'),
]
