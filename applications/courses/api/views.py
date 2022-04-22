from datetime import datetime
from xmlrpc.client import Boolean

from django.db.models import QuerySet

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import (
    CourseAsigned,
    CourseSchedule,
    CourseSession
)

from .serializers import (
    CourseAsignedSerializer,
    CourseScheduleSerializer,
    CourseSessionSerializer
)

class CourseAsignedView(APIView):

    serializer_class = CourseAsignedSerializer
    permission_classes = [ IsAdminUser ]

    def get_queryset(self, pk=None) -> QuerySet:
        
        if pk:
            return CourseAsigned.objects.all().filter( id = pk ).first()
        else:
            return CourseAsigned.objects.all()

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

