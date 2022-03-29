
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from applications.locations.models import Location
from .serializers import (
    CreateLocationSerializer,
    GetAllLocationsSerializer
)

class CreateLocationView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class   = CreateLocationSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                'message':'Sede creada',
                'data': response.data
            },
            status=status.HTTP_200_OK
        )

class GetAllLocationsView(ListAPIView):
    #permission_classes = [IsAdminUser]
    serializer_class   = GetAllLocationsSerializer
    queryset = Location.objects.all()
