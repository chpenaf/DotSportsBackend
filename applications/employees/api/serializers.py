import datetime

from rest_framework import serializers
from rest_framework.request import Request

from applications.employees.models import Employee
from applications.locations.models import Location
from applications.locations.api.serializers import GetLocationSerializer
from applications.users.models import User
from applications.users.api.serializers import UserSerializer

class CreateEmployeeSerializer(serializers.Serializer):

    doc_num = serializers.CharField(max_length=10)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    date_of_birth = serializers.DateField()
    sex = serializers.CharField(max_length=1)
    job = serializers.CharField(max_length=2)
    hire_date = serializers.DateField()
    id_location = serializers.IntegerField()
    email = serializers.EmailField()
    password = serializers.CharField(max_length=250)
    avatar = serializers.ImageField()

    def create(self, validated_data):

        user: User = User.objects.create(
            doc_num=validated_data['doc_num'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=True,
            avatar=validated_data['avatar'],
        )
        user.set_password(validated_data['password'])
        user.save()

        id_location = validated_data['id_location']

        location: Location = Location.objects.all().filter( 
                                id = id_location ).first()

        created_by = None
        request: Request = self.context.get('request')
        if request and hasattr(request,'user'):
            created_by = request.user

        employee: Employee = Employee.objects.create(
            doc_num=validated_data['doc_num'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            sex=validated_data['sex'],
            job=validated_data['job'],
            hire_date=validated_data['hire_date'],
            location=location,
            user=user,
            is_active=True,
            created_by=created_by,
            created_at=datetime.datetime.now()
        )

        employee.save()

        return validated_data
    

class UpdateEmployeeSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    doc_num = serializers.CharField(max_length=10)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    date_of_birth = serializers.DateField()
    sex = serializers.CharField(max_length=1)
    job = serializers.CharField(max_length=2)
    hire_date = serializers.DateField()
    id_location = serializers.IntegerField()
    email = serializers.EmailField()
    avatar = serializers.ImageField(required=False)


    def update(self, instance, validated_data):

        employee: Employee = instance

        id_location = validated_data['id_location']
        location: Location = Location.objects.all().filter( id = id_location ).first()

        user: User = employee.user

        updated_by = None
        request: Request = self.context.get('request')
        if request and hasattr(request,'user'):
            updated_by = request.user

        employee.doc_num = validated_data['doc_num']
        employee.first_name = validated_data['first_name']
        employee.last_name = validated_data['last_name']
        employee.date_of_birth = validated_data['date_of_birth']
        employee.sex = validated_data['sex']
        employee.job = validated_data['job']
        employee.hire_date = validated_data['hire_date']
        employee.location = location
        employee.updated_by = updated_by
        employee.updated_at = datetime.datetime.now()
        employee.save()

        if validated_data['email']:
            user.email = validated_data['email']

        if validated_data.get('avatar'):
            user.avatar = validated_data['avatar']

        user.save()

        return validated_data


class ListEmployeesSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    job_name = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id',
            'avatar',
            'doc_num',
            'full_name',
            'email',
            'job_name',
            'location',
            'hire_date',
            'is_active'
        ]

    def get_full_name(self, employee: Employee) -> str:
        return employee.get_full_name( )

    def get_avatar(self, employee:Employee) -> str:
        request: Request = self.context.get('request')
        if employee.user.avatar:
            avatar  = employee.user.avatar.url
            return request.build_absolute_uri(avatar)
        return ''
    
    def get_email(self, employee: Employee) -> str:
        return employee.user.email;

    def get_job_name(self, employee: Employee) -> str:
        if ( employee.job == 'AD'):
            return 'Administrador'
        elif ( employee.job == 'RE'):
            return 'Recepcionista'
        else:
            return 'Otro'

    def get_location(self, employee: Employee) -> str:
        return employee.location.name

class GetEmployeeSerializer(serializers.ModelSerializer):

    location = GetLocationSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = [
            'id',
            'doc_num',
            'first_name',
            'last_name',
            'date_of_birth',
            'sex',
            'job',
            'hire_date',
            'location',
            'user'
        ]
