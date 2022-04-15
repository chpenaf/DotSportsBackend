from datetime import datetime

from django.db.models import QuerySet
from django.forms import ValidationError

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from applications.users.models import User

from ..models import Application
from .serializers import AppsSerializer

@api_view(['GET'])
def get_now(request: Request):

    if request.method == 'GET':

        return Response(
            {
                'datetime': datetime.now(),
                'date': datetime.now().date(),
                'time': datetime.now().time()
            }, status=status.HTTP_200_OK
        )

class GetApps(ListAPIView):

    permission_classes = [ IsAuthenticated ]
    serializer_class = AppsSerializer

    def get_queryset(self, request: Request) -> QuerySet:

        if request and hasattr(request,'user'):
            user:User=request.user
            if user.is_superuser:
                return Application.objects.all().filter(admin=True)
            elif user.is_staff:
                return Application.objects.all().filter(staff=True)
            elif not user.is_staff and not user.is_superuser:
                return Application.objects.all().filter(member=True)
    
    def list(self, request: Request) -> Response:

        app_serializer = self.serializer_class(
            self.get_queryset(request).order_by('position'),
            context={'request':request},
            many=True
        )

        return Response(
            app_serializer.data,
            status=status.HTTP_200_OK
        )


class ApplicationAPIView(APIView):

    permission_classes = [ IsAdminUser ]

    def get_object(self, obj_id):
        try:
            return Application.objects.get(id=obj_id)
        except (Application.DoesNotExist, ValidationError):
            raise status.HTTP_400_BAD_REQUEST
    
    def validate_ids(self, id_list):
        for id in id_list:
            try:
                Application.objects.get(id=id)
            except (Application.DoesNotExist, ValidationError):
                raise status.HTTP_400_BAD_REQUEST
        return True
    
    def put(self, request, *args, **kwargs):
        
        instances = []
        
        for line in request.data:

            id = 0
            app: Application 
            
            if line['id']:
                id = line['id']

            if id > 0:


                app = Application.objects.all().filter(id = id).first()

                if app:

                    if line['name']:
                        app.name = line['name']

                    if line['path']:
                        app.path = line['path']
                    
                    if line['icon']:
                        app.icon = line['icon']
                    
                    if line['text']:
                        app.text = line['text']
                    
                    if line['position']:
                        app.position = line['position']

                    app.admin = line['admin']
                    app.staff = line['staff']
                    app.member = line['member']

                    app.save()

                else:
                    return Response(
                        {
                            'ok':False,
                            'message':'Not Found'
                        }, status=status.HTTP_404_NOT_FOUND
                    )
            
            else:

                app = Application.objects.create(
                    name = line['name'],
                    path = line['path'],
                    icon = line['icon'],
                    text = line['text'],
                    position = line['position'],
                    admin = line['admin'],
                    staff = line['staff'],
                    member = line['member']
                )

                app.save()

            instances.append(app)

        serializer = AppsSerializer(instances, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk=None):
        
        app: Application = Application.objects.all().filter(id=pk).first()

        if app:
            app.delete()
            return Response(
                {
                    'ok':True,
                    'message':'Application deleted'
                }, status=status.HTTP_200_OK
            )

        else:
            return Response(
                {
                    'ok':False,
                    'message':'Application not found'
                }, status=status.HTTP_404_NOT_FOUND
            )