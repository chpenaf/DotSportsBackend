from django.db.models import QuerySet

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.locations.models import Location
from ..models import (
    Service,
    Catalog,
    Course,
    Course_Level,
    Service_Subcategory
)
from .serializers import (
    ServiceSerializer,
    CourseSerializer,
    CourseLevelSerializer,
    CatalogSerializer,
    ServiceSubcategorySerializer
)

class ServiceView(APIView):

    serializer_class = ServiceSerializer

    def get_queryset(self, pk=None) -> QuerySet:
        if not pk:
            return Service.objects.all()
        else:
            return Service.objects.all().filter( id = pk ).first()

    def post(self, request: Request) -> Response:
        """
            Create one or many services
        """

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
    
    def get(self, request: Request, pk :int=None) -> Response:
        """
            Return one or all of services
        """
        if pk:
            many=False
        else:
            many=True

        serializer = self.serializer_class(
            self.get_queryset( pk ),
            many=many
        )
        
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, pk :int=None) -> Response:
        """
            Update one service
        """
        serializer = self.serializer_class(
            self.get_queryset( pk ),
            data=request.data
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

    def delete(self, request: Request, pk :int=None) -> Response:
        """
            Delete one service
        """
        service: Service = self.get_queryset( pk )

        if service:
            service.delete()
            return Response(
                {
                    'ok':True,
                    'message':'Service delete'
                }, status=status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    'ok':False,
                    'message':'Service not found'
                }, status=status.HTTP_404_NOT_FOUND
            )

class SubcategoryView(APIView):

    serializer_class = ServiceSubcategorySerializer

    def get_queryset(self, pk=None) -> QuerySet:
        if pk:
            return Service_Subcategory.objects.all().filter(
                id = pk 
            ).first()
        else:
            return Service_Subcategory.objects.all()

    def post(self, request):
        pass

    def get(self, request, pk=None):
        pass

    def put(self, request, pk=None):
        pass

    def delete(self, request, pk=None) -> Response:
        subcategory: Service_Subcategory = self.get_queryset( pk )
        if subcategory:
            subcategory.delete()
            return Response(
                {
                    'ok':True,
                    'message':'Subcategory delete'
                }, status=status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    'ok':False,
                    'message':'Subcategory not found'
                }, status=status.HTTP_404_NOT_FOUND
            )


class CatalogView(APIView):

    serializer_class = CatalogSerializer

    def get_queryset(self, id_location:int=None) -> QuerySet:
        if id_location:
            location: Location = Location.objects.all().filter(
                id = id_location
            ).first()
            if location:
                return Catalog.objects.all().filter(
                    location = location
                ).first()
            else:
                return None
        else:
            return Catalog.objects.all()
        


    def get(self, request: Request, id_location :int ) -> Response:
        """
            Get catalog by location
        """
        serializer = self.serializer_class(
            self.get_queryset(id_location)
        )

        return Response(
            serializer.data,
            status.HTTP_200_OK
        )