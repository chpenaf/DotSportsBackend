from dataclasses import field
from rest_framework import serializers

from applications.locations.models import Location, Pool

class CreatePoolSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Pool
        fields = [
            'name',
            'id_location',
            'lanes',
            'width',
            'length',
            'min_depth',
            'max_depth',
            'is_available',
            'pool'
        ]

class CreateLocationSerializer(serializers.ModelSerializer):

    pools = CreatePoolSerializer(read_only=True, many=True)

    class Meta:
        model  = Location
        fields = [
            'name',
            'address',
            'id_city',
            'city',
            'id_region',
            'region',
            'phone',
            'image',
            'pools'
        ]

class GetAllLocationsSerializer(serializers.ModelSerializer):

    pools = CreatePoolSerializer(read_only=True, many=True)
    full_address = serializers.SerializerMethodField()

    class Meta:
        model = Location
        fields = [
            'id',
            'name',
            'address',
            'id_city',
            'city',
            'id_region',
            'region',
            'phone',
            'image',
            'full_address',
            'pools'
        ]
    
    def get_full_address(self, location:Location):
        return location.get_address()