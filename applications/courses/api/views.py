from datetime import datetime, timedelta

from django.db.models import QuerySet

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.locations.models import Location
from applications.planning.models import Calendar, Slot
from applications.schedule.models import (
    Schedule, 
    Schedule_Day, 
    Schedule_Slot
)

from applications.schedule.api.serializers import ScheduleSlotSerializer

from ..models import (
    CourseAssigned,
    CourseSchedule,
    CourseSession
)

from .serializers import (
    CourseAssignedSerializer,
    CourseScheduleSerializer,
    CourseSessionSerializer
)

class CourseAssignedView(APIView):

    serializer_class = CourseAssignedSerializer
    permission_classes = [ IsAdminUser ]

    def get_queryset(self, pk=None, id_location=None) -> QuerySet:
        
        if pk:
            return CourseAssigned.objects.all().filter( id = pk ).first()
        if id_location:
            location: Location = Location.objects.all().filter(
                id = id_location
            ).first()
            return CourseAssigned.objects.all().filter(
                location = location
            )
        else:
            return CourseAssigned.objects.all()

    def post(self,request: Request) -> Response:
        
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
    
    def put(self, request: Request, pk=None) -> Response:

        serializer = self.serializer_class(
            self.get_queryset(pk),
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
    
    def get(self, request: Request, pk=None, id_location=None) -> Response:
        
        many = False
        
        if not pk:
            many = True
        
        if id_location:
            many = True
        
        serializer = self.serializer_class(
            self.get_queryset(pk,id_location),
            many=many
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )



class CourseScheduleView(APIView):

    serializer_class = CourseScheduleSerializer
    permission_classes = [ IsAdminUser ]

    def get_queryset(self, pk=None) -> QuerySet:
        
        if pk:
            return CourseSchedule.objects.all().filter( id = pk ).first()
        else:
            return CourseSchedule.objects.all()

    def post(self, request:Request) -> Response:
        
        serializer = self.serializer_class(
            data = request.data,
            many = True
        )

        if serializer.is_valid():
            serializer.save()
            list_schedule: list = serializer.data
            self.build_course_sessions(list_schedule)

            return Response(
                serializer.data,
                status.HTTP_200_OK
            )
    
        else:
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST
            )
    
    def get(self, request: Request, pk=None) -> Response:

        serializer = self.serializer_class(
            CourseSchedule.objects.all().filter(
                course_assigned = CourseAssigned.objects.all().filter(
                    id = pk
                ).first()
            ),
            many=True
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )

    def delete(self, request: Request, pk=None):

        course: CourseAssigned = CourseAssigned.objects.all().filter(
            id = pk
        ).first()

        if course:

            course.delete()
            return Response(
                {
                    'ok':True,
                    'message':'Course deleted'
                }, status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    'ok':False,
                    'message':'Course not found'
                }, status.HTTP_404_NOT_FOUND
            )

    def build_course_sessions(self, data: list):
        id_course = data[0].get('course_assigned')
        course: CourseAssigned = CourseAssigned.objects.all().filter(
            id = id_course
        ).first()

        index = 0
        sessions = course.num_sessions
        currdate = course.startdate
        session_list = list()

        while index < sessions:

            calendar: Calendar = Calendar.objects.all().filter(
                location = course.location,
                date = currdate
            ).first()

            for item in data:
                schedule: CourseSchedule = CourseSchedule.objects.all().filter(
                    id = item.get('id')
                ).first()

                if calendar.day_week == schedule.weekday:
                    slot: Slot = Slot.objects.all().filter(
                        calendar = calendar,
                        starttime = schedule.slot.starttime
                    ).first()

                    if slot:

                        session = CourseSession.objects.create(
                            course_assigned = course,
                            course_schedule = schedule,
                            date = calendar,
                            slot = slot
                        )

                        session.save()
                        session_list.append(session)
                        index += 1
            
            currdate += timedelta(days=1)



class CourseSessionView(APIView):

    serializer_class = CourseSessionSerializer
    permission_classes = [ IsAdminUser ]

    def get_queryset(self, pk=None, year=None, month=None, day=None) -> QuerySet:
        
        if pk:
            return CourseSession.objects.all().filter( id = pk ).first()
        elif year and month and day:
            date = datetime(year, month, day)
            return CourseSession.objects.all().filter(
                date = Calendar.objects.all().filter(
                    date = date
                ).first()
            )
        else:
            return CourseSession.objects.all()

    def post(self, request:Request) -> Response:

        serializer = self.serializer_class(
            data = request.data,
            many = True
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
    
    def get(self, request: Request, pk=None, year=None, month=None, day=None) -> Response:
        
        many = False
        
        if not pk:
            many = True
        elif year and month and day:
            many = True
        
        serializer = self.serializer_class(
            self.get_queryset(pk, year, month, day),
            many=many
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )


@api_view(['GET'])
def get_schedule_week(request: Request, pk: int = None) -> Response:

    if request.method == 'GET':

        course: CourseAssigned = CourseAssigned.objects.all().filter(
            id = pk
        ).first()

        if not course:
            return Response(
                {
                    'ok': False,
                    'message': 'Course not found'
                }, status=status.HTTP_404_NOT_FOUND
            )

        schedule: Schedule = Schedule.objects.all().filter(
            location = course.location
        ).first()

        if not schedule:
            return Response(
                {
                    'ok': False,
                    'message': 'Schedule not found'
                }, status=status.HTTP_404_NOT_FOUND
            )

        serializer = ScheduleSlotSerializer(
            Schedule_Slot.objects.all().filter(
                schedule_day__in = Schedule_Day.objects.all().filter(
                    schedule = schedule,
                    daytype__in = ['WD','SA']
                )
            ),
            many=True
        )

        return Response(
            serializer.data, 
            status.HTTP_200_OK
        )