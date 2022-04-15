from rest_framework.serializers import ModelSerializer

from ..models import Application

class AppsSerializer(ModelSerializer):

    class Meta:
        model  = Application
        fields = [
            'id',
            'name',
            'path',
            'icon',
            'text',
            'position',
            'admin',
            'staff',
            'member'
        ]
    
    def update(self, instance, validated_data):
        print('VALIDATED_DATA: ',validated_data)
        return validated_data