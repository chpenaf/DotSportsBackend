
import datetime

from rest_framework import status
from rest_framework.request import Request
from rest_framework.generics import (
    CreateAPIView, 
    ListAPIView, 
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from applications.locations.models import Location
from .serializers import (
    CreateLocationSerializer,
    GetAllLocationsSerializer,
    GetLocationToSelectSerializer,
    UpdateLocationSerializer
)


class CreateLocationView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class   = CreateLocationSerializer

    def post(self, request:Request):

        data = request.data
        data.update({ 'created_by': request.user.id })

        serializer = self.serializer_class(data = data)

        if serializer.is_valid():                      
            serializer.save()
            return Response(
                {
                    'message':'Sede creada',
                    'data': serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

class GetAllLocationsView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class   = GetAllLocationsSerializer
    queryset = Location.objects.all().filter(state=True)

class CancelLocationView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UpdateLocationSerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter(state = True)

    def delete(self,request:Request,pk=None):
        location: Location = self.get_queryset().filter(id = pk).first()
        if location:
            location.state = False
            location.canceled_at = datetime.datetime.now()
            location.canceled_by = request.user
            location.save()
            return Response(
                {
                    'message':'Sede anulada'
                }, status=status.HTTP_200_OK
            )

        return Response(
            {
                'message':'No se efectuó anulación'
            }, status=status.HTTP_400_BAD_REQUEST
        )

class UpdateLocationView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UpdateLocationSerializer

    def get_queryset(self, pk = None):
        return self.get_serializer().Meta.model.objects.filter(state = True).filter(id = pk).first()

    def patch(self, request, pk=None):
        if self.get_queryset(pk):
            location_serializer = self.serializer_class(self.get_queryset(pk))
            return Response(location_serializer.data, status=status.HTTP_200_OK)
        return Response({
            'error':'No se encontró sede con datos ingresados'
            }, status=status.HTTP_400_BAD_REQUEST
        )
    
    def put(self, request:Request, pk=None):
    
        if self.get_queryset(pk):
            location_serializer = self.serializer_class(self.get_queryset(pk),data = request.data)
            if location_serializer.is_valid():
                location_serializer.save()
                location: Location = self.get_queryset(pk)
                location.updated_by = request.user
                location.updated_at = datetime.datetime.now()
                location.save()
                return Response(
                    location_serializer.data,
                    status= status.HTTP_200_OK
                )
            else:
                return Response(
                    location_serializer.errors,
                    status= status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'message':'No se encontraron sedes con los parámetros ingresados'
                },
                status= status.HTTP_400_BAD_REQUEST
            )

class GetLocationToSelectView(ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class   = GetLocationToSelectSerializer
    queryset = Location.objects.all().filter(state = True)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)