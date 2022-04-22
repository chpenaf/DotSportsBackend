from datetime import timedelta

from django.db.models import QuerySet

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.locations.models import Location
from applications.planning.models import Calendar, Slot

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
            ).first()
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
    
    def get(self, request: Request, pk=None, id_location=None) -> Response:
        
        many = False
        
        if not pk:
            many = True
        
        if id_location:
            many = False
        
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
        
        many = False
        
        if not pk:
            many = True
        
        serializer = self.serializer_class(
            self.get_queryset(pk),
            many=many
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
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

    def get_queryset(self, pk=None) -> QuerySet:
        
        if pk:
            return CourseSession.objects.all().filter( id = pk ).first()
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
    
    def get(self, request: Request, pk=None) -> Response:
        
        many = False
        
        if not pk:
            many = True
        
        serializer = self.serializer_class(
            self.get_queryset(pk),
            many=many
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )