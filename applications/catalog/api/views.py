from django.db.models import QuerySet

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
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


class CourseView(APIView):

    serializer_class = CourseSerializer
    permission_classes = [ IsAuthenticated ]

    def post(self, request: Request, id_location: int = None) -> Response:

        serializer = self.serializer_class(
            data=request.data
        )

        location: Location = Location.objects.all().filter( id = id_location ).first()
        
        if not location:
            return Response(
                {
                    'ok': False,
                    'message': 'Location not found'
                },
                status.HTTP_400_BAD_REQUEST
            )

        catalog: Catalog = Catalog.objects.all().filter(
                location = location
            ).first()

        if not catalog:
            return Response(
                {
                    'ok': False,
                    'message': 'Catalog not found'
                },
                status.HTTP_400_BAD_REQUEST
            )

        if serializer.is_valid():
            serializer.save()

            course: Course = serializer.instance
            catalog.courses.add(course)
            catalog.save()

            return Response(
                serializer.data,
                status.HTTP_200_OK
            )
        
        else:
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST
            )

    def put(self, request: Request) -> Response:
        
        pk = request.data.get('id')

        if pk:
            instance = Course.objects.all().filter( id = pk ).first()

        if not instance:
            return Response(
                {
                    'ok': False,
                    'message': 'Course not found'
                },
                status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.serializer_class(
            instance=instance,
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
    
    def delete(self, request:Request, pk:int = None ) -> Response:

        if pk:
            instance = Course.objects.all().filter( id = pk ).first()

        if instance:

            instance.delete()
            return Response(
                {
                    'ok': True,
                    'message': 'Course deleted'
                },
                status.HTTP_200_OK
            )

        else:
            return Response(
                {
                    'ok': False,
                    'message': 'Course not found'
                },
                status.HTTP_404_NOT_FOUND
            )
        


        

class LevelView(APIView):

    serializer_class = CourseLevelSerializer
    permission_classes = [ IsAuthenticated ]

    def post(self, request: Request):

        instances = list()

        for item in request.data:

            if item.get('id'):

                level: Course_Level = Course_Level.objects.all().filter(
                    id = item.get('id')
                ).first()

                serializer = self.serializer_class(
                    instance=level,
                    data=item
                )

                if serializer.is_valid():
                    serializer.save()
                    instances.append(serializer.instance)
                else:
                    return Response(
                        serializer.errors,
                        status.HTTP_400_BAD_REQUEST
                    )
            
            else:

                serializer = self.serializer_class(
                    data=item
                )

                if serializer.is_valid():
                    serializer.save()
                    instances.append(serializer.instance)
                else:
                    return Response(
                        serializer.errors,
                        status.HTTP_400_BAD_REQUEST
                    )
        
        if instances:

            serializer = self.serializer_class(
                instance=instances,
                many=True
            )

            return Response(
                serializer.data,
                status.HTTP_200_OK
            )

        else:
            return Response(
                {
                    'ok': False,
                    'message': 'Nothing happened'
                }, status.HTTP_400_BAD_REQUEST
            )
            

            
    
    def delete(self, request: Request, pk: int=None):

        level: Course_Level = Course_Level.objects.all().filter( pk = pk ).first()

        if level:
            level.delete()
            return Response(
                {
                    'ok': True,
                    'message': 'Borrado correctamente'
                }, status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    'ok': False,
                    'message': 'Nivel no encontrado'
                }, status.HTTP_400_BAD_REQUEST
            )

class CatalogView(APIView):

    serializer_class = CatalogSerializer
    permission_classes = [ IsAuthenticated ]

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