from django.db.models import QuerySet

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import CapacityPool
from .serializers import (
    CapacityPoolSerializer,
    CapacityPoolListSerializer
)

class CapacityPoolView(APIView):

    serializer_class = CapacityPoolSerializer
    permission_classes = [ IsAdminUser ]

    def get_queryset(self, pk:int=None) -> QuerySet:
        if pk:
            return CapacityPool.objects.all().filter(
                id = pk
            ).first()
        else:
            return CapacityPool.objects.all()
    
    def post(self, request: Request) -> Response:
        
        serializer = self.serializer_class(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST
            )
    
    def get(self, request: Request) -> Response:
        
        serializer = CapacityPoolListSerializer(
            instance = CapacityPool.objects.all(),
            many = True
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def put(self, request: Request, pk: int = None) -> Response:

        serializer = self.serializer_class(
            instance = self.get_queryset(pk=pk),
            data = request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status.HTTP_200_OK
            )

        else:
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST
            )
    
    def delete(self, request: Request, pk: int = None) -> Response:

        capacity_pool: CapacityPool = self.get_queryset(pk=pk)
        
        if capacity_pool:
            capacity_pool.delete()
            return Response(
                {
                    'ok': True,
                    'message':'Object deleted'
                }, status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    'ok': False,
                    'message': 'Not found'
                }, status.HTTP_404_NOT_FOUND
            )