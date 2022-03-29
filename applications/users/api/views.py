from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from ..models import User
from .serializers import UserSerializer

@api_view(['GET'])
def currentUser(request: Request):

    if request.method == 'GET':
        
        user_serializer = UserSerializer( request._user, context={'request':request} )

        return Response(
            user_serializer.data,
            status=status.HTTP_200_OK
        )