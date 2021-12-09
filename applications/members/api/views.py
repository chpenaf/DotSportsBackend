from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from .serializers import SignUpSerializer

@api_view(['POST'])
def signup_member(request: Request):

    if request.method == 'POST':

        signup_serializer = SignUpSerializer(data=request.data)

        if signup_serializer.is_valid():

            signup_serializer.save()

            return Response( 
                signup_serializer.data,
                status=status.HTTP_201_CREATED)
        
        else:
            return Response(
                signup_serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)