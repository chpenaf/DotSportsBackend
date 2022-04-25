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
from applications.planning.models import Calendar
from ..models import (
    Schedule,
    Schedule_Day,
    Schedule_Slot
)
from .serializers import (
    ListScheduleSerializer,
    ScheduleSerializer,
    ScheduleDaySerializer,
    ScheduleDaySerializer2,
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
            serializer_response = ScheduleDaySerializer2(
                serializer.instance,
                many=True
            )
            return Response(
                serializer_response.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def get(self, request: Request, id_location: int = None ) -> Response:

        if id_location:
            location: Location = Location.objects.all().filter(
                id = id_location
            ).first()

        if not location:
            return Response(
                {
                'ok':False,
                'message':'Location not found'
                }, status.HTTP_404_NOT_FOUND
            )

        serializer = ScheduleDaySerializer(
            Schedule_Day.objects.all().filter(
                schedule = Schedule.objects.all().filter(
                    location = location
                ).first()
            ),
            many=True
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
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

class ScheduleView(APIView):

    permission_classes = [ IsAdminUser ]
    serializer_class = ScheduleSerializer

    def post(self, request:Request) -> Response:

        data = request.data

        # Location
        if(data.get('location')):
            location: Location = Location.objects.all().filter(
                id = data.get('location')
            ).first()

            if not location:
                return Response(
                {
                    'ok':False,
                    'message':'Location not found'
                },
                status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
            {
                'ok':False,
                'message':'Location is required'
            },
            status=status.HTTP_400_BAD_REQUEST
            )
        
        # Begin Validity
        if(data.get('begin_validity')):
            begin_validity = datetime.strptime(
                data.get('begin_validity'),
                    '%Y-%m-%d')
        else:
            return Response(
                {
                    'ok':False,
                    'message':'Begin validity is required'
                },
                status=status.HTTP_400_BAD_REQUEST
                )
        
        # End Validity
        if(data.get('end_validity')):
            end_validity = datetime.strptime(
                data.get('end_validity'),
                    '%Y-%m-%d')
        else:
            return Response(
                {
                    'ok':False,
                    'message':'End validity is required'
                },
                status=status.HTTP_400_BAD_REQUEST
                )
        
        # Valida si debe crear o modificar 
        if(data.get('id')):
            # UPDATE
            schedule: Schedule = Schedule.objects.all().filter(
                id = data.get('id')
            ).first()

            schedule.location = location
            schedule.begin_validity = begin_validity.date()
            schedule.end_validity = end_validity.date()
            schedule.save()

            list_days: list = data.get('days')

            for item in list_days:
                daytype = item.get('daytype')
                is_open = item.get('is_open')

                day: Schedule_Day = Schedule_Day.objects.all().filter(
                    schedule=schedule,
                    daytype=daytype
                ).first()

                day.is_open = is_open
                day.save()

                list_slots: list = item.get('slots')
                index_slot = 1
                for item_slot in list_slots:

                    slot: Schedule_Slot = Schedule_Slot.objects.all().filter(
                        schedule_day=day,
                        slot=index_slot
                    ).first()

                    if slot:
                        slot.starttime=item_slot.get('starttime')
                        slot.endtime=item_slot.get('endtime')
                        slot.save()

                    else:
                        slot: Schedule_Slot = Schedule_Slot.objects.create(
                           schedule_day=day,
                           slot=index_slot,
                           starttime=item_slot.get('starttime'),
                           endtime=item_slot.get('endtime')
                        )
                        slot.save()
                    
                    index_slot += 1
            
        else:
            # CREATE
            schedule: Schedule = Schedule.objects.create(
                location=location,
                begin_validity=begin_validity,
                end_validity=end_validity
            )
            schedule.save()

            list_days: list = data.get('days')

            for item in list_days:
                daytype = item.get('daytype')
                is_open = item.get('is_open')

                day: Schedule_Day = Schedule_Day.objects.create(
                    schedule=schedule,
                    daytype=daytype,
                    is_open=is_open
                )
                day.save()

                list_slots: list = item.get('slots')
                index_slot = 1
                for item_slot in list_slots:
                    slot: Schedule_Slot = Schedule_Slot.objects.create(
                        schedule_day=day,
                        slot=index_slot,
                        starttime=item_slot.get('starttime'),
                        endtime=item_slot.get('endtime')
                    )
                    slot.save()
                    index_slot += 1
        
        Calendar.fill_calendar(location,begin_validity,end_validity)

        return Response({
            'ok':True
        })