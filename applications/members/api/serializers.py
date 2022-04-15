from dataclasses import fields
import datetime
from rest_framework import serializers
from rest_framework.request import Request

from applications.members.models import Member
from applications.users.api.serializers import UserSerializer
from applications.users.models import User

class SignUpSerializer(serializers.Serializer):

    doc_num = serializers.CharField(max_length=10)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    date_of_birth = serializers.DateField()
    sex = serializers.CharField(max_length=1)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=250)

    def create(self, validated_data):
        
        user: User = User.objects.create(
            doc_num=validated_data['doc_num'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            )
        user.set_password(validated_data['password'])
        user.save()

        member: Member = Member.objects.create(
            doc_num=validated_data['doc_num'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            sex=validated_data['sex'],
            user=user
        )

        member.save()

        return validated_data

class ListSerializer(serializers.ModelSerializer):

    avatar = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model  = Member
        fields = [
            'id',
            'avatar',
            'doc_num',
            'full_name',
            'age',
            'email',
            'status'
        ]
    
    def get_avatar(self, member: Member) -> str:
        request: Request = self.context.get('request')
        if member.user.avatar:
            avatar = member.user.avatar.url
            return request.build_absolute_uri(avatar)
        return False
    
    def get_full_name(self, member: Member) -> str:
        return member.get_short_name()

    def get_age(self, member: Member) -> str:
        return member.get_age()
    
    def get_email(self, member: Member) -> str:
        return member.user.email;

class CreateUpdateSerializer(serializers.Serializer):

    doc_num = serializers.CharField(max_length=10)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    date_of_birth = serializers.DateField()
    sex = serializers.CharField(max_length=1)
    status = serializers.CharField(max_length=2)
    email = serializers.EmailField()
    avatar = serializers.ImageField(required=False)
    password = serializers.CharField(max_length=250, required=False)

    def create(self, validated_data):

        request: Request = self.context.get('request')

        user: User = User.objects.create(
            doc_num=validated_data['doc_num'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_staff=False,
        )

        if validated_data.get('avatar'):
            user.avatar = validated_data['avatar']

        user.set_password(validated_data['password'])
        user.save()

        created_by = None
        if request and hasattr(request,'user'):
            created_by = request.user
        
        member: Member = Member.objects.create(
            doc_num=validated_data['doc_num'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            sex=validated_data['sex'],
            status=validated_data['status'],
            user=user,
            created_by=created_by,
            created_at=datetime.datetime.now()
        )

        member.save()

        return validated_data

    def update(self, instance, validated_data):

        request: Request = self.context.get('request')
        member: Member = instance
        user: User = member.user

        updated_by = None
        if request and hasattr(request,'user'):
            updated_by = request.user
        
        member.doc_num = validated_data['doc_num']
        member.first_name = validated_data['first_name']
        member.last_name = validated_data['last_name']
        member.date_of_birth = validated_data['date_of_birth']
        member.sex = validated_data['sex']
        member.status = validated_data['status']
        member.updated_by = updated_by
        member.updated_at = datetime.datetime.now()
        member.save()

        user.doc_num = member.doc_num
        user.first_name = member.first_name
        user.last_name = member.last_name

        if validated_data.get('email'):
            user.email = validated_data['email']
        
        if validated_data.get('avatar'):
            user.avatar = validated_data['avatar']

        user.save()

        return validated_data

class RetrieveSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)

    class Meta:
        model  = Member
        fields = [
            'id',
            'doc_num',
            'first_name',
            'last_name',
            'date_of_birth',
            'sex',
            'status',
            'user'
        ]
