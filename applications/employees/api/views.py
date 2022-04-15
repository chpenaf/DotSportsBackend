import datetime
from django.db.models import QuerySet

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    DestroyAPIView
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from applications.users.models import User
from ..models import Employee
from .serializers import (
    CreateEmployeeSerializer,
    GetEmployeeSerializer,
    UpdateEmployeeSerializer,
    ListEmployeesSerializer
)



class ListEmployeesView(ListAPIView):
    permission_classes = [ IsAdminUser ]
    serializer_class   = ListEmployeesSerializer

    def get_queryset(self) -> QuerySet:
        return Employee.objects.all().filter( is_active = True )

    def list(self, request) -> Response: 
        employee_serializer = self.serializer_class(
            self.get_queryset(), 
            context={ 'request': request },
            many=True
        )

        return Response(
            employee_serializer.data,
            status=status.HTTP_200_OK
        )





class CreateEmployeeView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class   = CreateEmployeeSerializer

    def create(self, request: Request, *args, **kwargs):

        employee_serializer = self.serializer_class(
            context = { 'request':request }, 
            data = request.data
        )

        if employee_serializer.is_valid():

            employee_serializer.save()

            return Response(
                employee_serializer.data, 
                status=status.HTTP_201_CREATED
            )
        
        else:
            return Response(
                employee_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )




class UpdateEmployeeView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class   = UpdateEmployeeSerializer

    def get_queryset(self, pk=None):
        return Employee.objects.filter( id = pk ).first()

    def put(self, request: Request, pk=None):

        if self.get_queryset(pk):
            employee_serializer = self.serializer_class(
                self.get_queryset(pk),
                context = { 'request': request },
                data = request.data
            )

            if employee_serializer.is_valid():
                employee_serializer.save()
                return Response(
                    employee_serializer.data,
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    employee_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

        else:
            return Response(
                {
                    'message': 'No se encontraron empleados con la clave indicada'
                }, status=status.HTTP_400_BAD_REQUEST
            )


class RetrieveEmployee(RetrieveAPIView):

    permission_classes = [IsAdminUser]
    serializer_class   = GetEmployeeSerializer

    def get_queryset(self, pk=None):
        return Employee.objects.filter( id = pk ).first()

    def get(self, request: Request, pk=None):
        
        if self.get_queryset(pk):
            employee_serializer = self.serializer_class(
                self.get_queryset(pk),
                context={'request':request}
            )

            return Response(
                    employee_serializer.data,
                    status=status.HTTP_200_OK
                )
        
        else:
            return Response(
                {
                    'ok' : False,
                    'message': 'No se encontraron empleados con la clave indicada'
                }, status=status.HTTP_400_BAD_REQUEST
            )

class RetrieveLogged(RetrieveAPIView):

    permission_classes = [ IsAuthenticated ]
    serializer_class = GetEmployeeSerializer

    def get_queryset(self, doc_num=None):
        return Employee.objects.filter( doc_num = doc_num ).first()

    def get(self, request: Request):

        if request and hasattr(request,'user'):
            myUser: User = request.user

            if self.get_queryset(myUser.doc_num):
                employee_serializer = self.serializer_class(
                    self.get_queryset(myUser.doc_num),
                    context= {'request':request}
                )
                return Response(
                    employee_serializer.data,
                    status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {
                        'ok' : False,
                        'message': 'No se encontró empleado del usuario logueado'
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {
                    'ok' : False,
                    'message': 'Error al recuperar empleado'
                }, status=status.HTTP_400_BAD_REQUEST
            )




class CancelEmployee(DestroyAPIView):
    
    permission_classes = [IsAdminUser]
    serializer_class   = GetEmployeeSerializer

    def get_queryset(self, pk=None):
        return Employee.objects.filter( id = pk ).first()

    def delete(self, request: Request, pk=None):

        if self.get_queryset(pk):
            employee: Employee = self.get_queryset(pk)
            if employee:
                employee.is_active = False;
                employee.canceled_at = datetime.datetime.now()
                employee.canceled_by = request.user
                employee.save()
                return Response(
                    {
                        'ok' : True,
                        'message' : 'Empleado anulado'
                    }, status=status.HTTP_200_OK
                )
        
        else:
            return Response(
                {
                    'ok' : False,
                    'message' : 'No se encontraron empleados con la clave indicada'
                }, status=status.HTTP_400_BAD_REQUEST
            )