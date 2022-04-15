import os
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import ( 
    smart_str, 
    force_str, 
    smart_bytes, 
    DjangoUnicodeDecodeError 
    )
from django.utils.http import ( 
    urlsafe_base64_decode, 
    urlsafe_base64_encode 
    )
from rest_framework import generics, status
from rest_framework.response import Response

from applications.utils import Util
from applications.users.models import User
from .serializers import (
    CheckDocumentNumberExistsSerializer,
    CheckEmailExistsSerializer,
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer
)

class CheckDocumentNumberExists(generics.GenericAPIView):
    serializer_class = CheckDocumentNumberExistsSerializer

    def post(self, request):

        doc_num = request.data.get('doc_num', '')

        if User.objects.filter(doc_num=doc_num).exists():
            return Response({
                'code': '0',
                'message': 'Documento ingresado ya existe en sistema'
            }, status=status.HTTP_200_OK)

        return Response({
                'code': '4',
                'message': 'Documento ingresado no existe en sistema'
        }, status=status.HTTP_200_OK)
        
class CheckEmailExists(generics.GenericAPIView):
    serializer_class = CheckEmailExistsSerializer

    def post(self, request):

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            return Response({
                'code': '0',
                'message': 'Email ingresado ya existe en sistema'
            }, status=status.HTTP_200_OK)

        return Response({
                'code': '4',
                'message': 'Email ingresado no existe en sistema'
        }, status=status.HTTP_200_OK)

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user:User = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            redirect_url = request.data.get('redirect_url', os.environ.get('FRONTEND_URL', '') + 'auth/change-password' )
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hola ' + user.get_short_name() + '! \nUsa el enlace de más abajo para restablecer tu contraseña  \n' + \
                absurl+"?redirect_url="+redirect_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Restablecer contraseña'}
            Util.send_email(data)
        return Response({'message': 'Se te ha enviado un link a tu correo para restablecer contraseña'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)