from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from .views import (
    CheckDocumentNumberExists,
    CheckEmailExists,
    PasswordTokenCheckAPI,
    RequestPasswordResetEmail,
    SetNewPasswordAPIView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('check-docnum-exists/', CheckDocumentNumberExists.as_view(), name="check-docnum_exists"), # Verifica si Rut existe
    path('check-email-exists/', CheckEmailExists.as_view(), name="check-email_exists"), # Verifica si Email existe
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"), # Envia mail con instrucciones
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'), # Valida Token
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete') # Restablece password
]