from datetime import datetime
from django.db.models import QuerySet

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from applications.members.api.serializers import (
    SignUpSerializer,
    ListSerializer,
    CreateUpdateSerializer,
    RetrieveSerializer
)

from applications.members.models import Member
from applications.users.models import User

@api_view(['POST'])
def signup_member(request: Request):

    if request.method == 'POST':

        signup_serializer = SignUpSerializer(data=request.data)

        if signup_serializer.is_valid():
            signup_serializer.save()
            return Response( 
                signup_serializer.data,
                status=status.HTTP_201_CREATED)
        
        else:
            return Response(
                signup_serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST)

class ListView(ListAPIView):

    permission_classes = [ IsAuthenticated ]
    serializer_class = ListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self) -> QuerySet:
        return Member.objects.all()

    def list(self, request) -> Response:
        member_serializer = self.serializer_class(
            self.filter_queryset(self.get_queryset()),
            context={'request': request},
            many=True
        )

        return Response(
            member_serializer.data,
            status=status.HTTP_200_OK
        )

class CreateView(CreateAPIView):

    permission_classes = [ IsAuthenticated ]
    serializer_class = CreateUpdateSerializer

    def create(self, request: Request, *args, **kwargs):
        member_serializer = self.serializer_class(
            context = { 'request': request },
            data = request.data
        )

        if member_serializer.is_valid():
            member_serializer.save()
            return Response(
                {
                    'ok': True,
                    'message':'Member created successfully'
                }, status=status.HTTP_200_OK
            )
        else:
            print(member_serializer.errors)
            return Response(
                {
                    'ok': False,
                    'message': member_serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )

class RetrieveView(RetrieveAPIView):

    permission_classes = [ IsAuthenticated ]
    serializer_class = RetrieveSerializer

    def get_queryset(self,pk=None) -> QuerySet:
        return Member.objects.all().filter( id = pk ).first()

    def get(self, request: Request, pk=None) -> Response:

        if self.get_queryset(pk):
            member_serializer = self.serializer_class(
                self.get_queryset(pk),
                context={'request':request}
            )
            return Response(
                member_serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'ok':False,
                    'message':'Member Not Found'
                }, status=status.HTTP_404_NOT_FOUND
            )

class UpdateView(UpdateAPIView):

    permission_classes = [ IsAuthenticated ]
    serializer_class = CreateUpdateSerializer

    def get_queryset(self,pk=None) -> QuerySet:
        return Member.objects.all().filter( id = pk ).first()
    
    def put(self, request: Request, pk=None) -> Response:

        if self.get_queryset(pk):
            member_serializer = self.serializer_class(
                self.get_queryset(pk),
                context = { 'request': request },
                data = request.data
            )

            if member_serializer.is_valid():
                member_serializer.save()
                return Response(
                    {
                        'ok':True,
                        'message':'Member updated successfully'
                    }, status=status.HTTP_200_OK
                )
            
            else:
                return Response(
                    {
                        'ok':False,
                        'message':member_serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        
        else:
            return Response(
                {
                    'ok':False,
                    'message':'Member Not Found'
                }, status=status.HTTP_404_NOT_FOUND
            )

class CancelView(DestroyAPIView):

    permission_classes = [ IsAuthenticated ]
    serializer_class = RetrieveSerializer

    def get_queryset(self,pk=None) -> QuerySet:
        return Member.objects.all().filter( id = pk ).first()
    
    def delete(self, request: Request, pk=None) -> Response:

        if self.get_queryset(pk):
            member: Member = self.get_queryset(pk)
            if member:
                member.status = 'IN'
                member.canceled_at = datetime.now()
                member.canceled_by = request.user
                member.save()
                return Response(
                    {
                        'ok' : True,
                        'message' : 'Member deactivated'
                    }, status=status.HTTP_200_OK
                )

        else:
            return Response(
                {
                    'ok':False,
                    'message':'Member Not Found'
                }, status=status.HTTP_404_NOT_FOUND
            )
    
class SelfInfoView(APIView):

    serializer_class = RetrieveSerializer
    permission_classes = [ IsAuthenticated ]

    def get(self, request:Request):

        if( request.user ):

            user: User = request.user
            
            serializer = self.serializer_class(
                Member.objects.all().filter(
                    doc_num = user.doc_num
                ).first(),
                context={'request':request}
            )

            return Response(
                serializer.data,
                status.HTTP_200_OK
            )

        else:
            return Response(
                {
                    'ok': False,
                    'message': 'User not found'
                },
                status.HTTP_400_BAD_REQUEST
            )