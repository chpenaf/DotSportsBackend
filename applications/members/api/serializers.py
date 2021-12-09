
from datetime import datetime
from rest_framework import serializers

from applications.members.models import Member
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