from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from ..models import User
from .serializers import UserSerializer, PasswordSerializer

@api_view(['GET'])
def currentUser(request: Request):

    if request.method == 'GET':
        
        user_serializer = UserSerializer( request._user, context={'request':request} )

        return Response(
            user_serializer.data,
            status=status.HTTP_200_OK
        )

class PasswordView(APIView):

    serializer_class = PasswordSerializer
    permission_classes = [ IsAuthenticated ]

    def post(self, request: Request) -> Response:

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user: User = request.user

            if user.check_password(serializer.validated_data.get('current')): 
                user.set_password(serializer.validated_data.get('newpass'))
                user.save()
                return Response(
                    {
                        'ok': True,
                        'message': 'Contraseña actualizada'
                    }, status.HTTP_200_OK
                )

            else:
                return Response(
                    {
                        'ok': False,
                        'message': 'Contraseña incorrecta'
                    }, status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {
                    'ok': False,
                    'message': serializer.errors
                }, status.HTTP_400_BAD_REQUEST
            )
        