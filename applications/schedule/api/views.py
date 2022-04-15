import json, os
from datetime import datetime

from django.db.models import QuerySet

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView
)
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.locations.models import Location

from ..models import (
    Schedule,
    Schedule_Day,
    Schedule_Slot
)
from .serializers import (
    ListScheduleSerializer,
    ScheduleSerializer,
    CreateScheduleDaySerializer,
    CreateSlotSerializer,
)

class ListView(ListAPIView):

    permission_classes = [ IsAdminUser ]
    serializer_class = ListScheduleSerializer

    def get_queryset(self, id) -> QuerySet:
        location = Location.objects.all().filter( id = id ).first()
        return Schedule.objects.all().filter( 
            location = location,
            begin_validity__lte = datetime.date( datetime.now()),
            end_validity__gte = datetime.date( datetime.now())
        )
    
    def list(self,request:Request, id) -> Response:
        schedule_serializer = self.serializer_class(
            self.get_queryset( id ),
            many=True
        )

        return Response(
            schedule_serializer.data,
            status=status.HTTP_200_OK
        )

class RetrieveView(RetrieveAPIView):

    permission_classes = [ IsAdminUser ]
    serializer_class = ListScheduleSerializer

    def get_queryset(self,pk=None) -> QuerySet:
        return Schedule.objects.all().filter( id = pk ).first()
    
    def get(self, request:Request, pk=None ) -> Response:
        schedule_serializer = self.serializer_class(
            self.get_queryset(pk),
            context={ 'request': request }
        )

        return Response(
            schedule_serializer.data,
            status=status.HTTP_200_OK
        )

@api_view(['GET'])
def getDayTypes(request:Request):

    if request.method == 'GET':

        json_data = list()

        for item in Schedule_Day.DAYS_CHOICES:
            json_data.append(
                { 'key':item[0], 'value':item[1]  }
            )

        return Response(
            json_data,
            status=status.HTTP_200_OK
        )

class ScheduleAPIView(APIView):

    permission_classes = [ IsAdminUser ]
    serializer_class = ScheduleSerializer

    def get_queryset(self, pk=None) -> QuerySet:
        if pk:
            return Schedule.objects.all().filter(id = pk).first()

    def post(self,request:Request) -> Response:

        serializer = self.serializer_class(
            context = { 'request': request },
            data = request.data
        )

        if serializer.is_valid():
            serializer.save()            
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self,request:Request,pk=None) -> Response:

        serializer = self.serializer_class(
            self.get_queryset(pk),
            context= { 'request': request },
            data= request.data
        )

        if serializer.is_valid():
            serializer.save()            
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class ScheduleDayApiView(APIView):

    permission_classes = [ IsAdminUser ]
    serializer_class = CreateScheduleDaySerializer

    def post(self, request):
        
        serializer = self.serializer_class(
            data=request.data,
            many=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

class ScheduleSlotApiView(APIView):

    permission_classes = [ IsAdminUser ]
    serializer_class = CreateSlotSerializer

    def post(self, request):

        print('REQUEST',request.data)

        serializer = self.serializer_class(
            data=request.data,
            many=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )