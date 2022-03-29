from rest_framework import serializers

from ..models import User

class UserSerializer( serializers.ModelSerializer ):

    full_name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'avatar',
            'is_staff'
        ]
    
    def get_avatar(self, user:User):
        request = self.context.get('request')
        if user.avatar:
            avatar  = user.avatar.url
            return request.build_absolute_uri(avatar)
        return False

    def get_full_name(self, user:User):
        return user.get_full_name()
