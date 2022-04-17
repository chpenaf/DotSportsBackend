from datetime import datetime

from rest_framework import serializers
from rest_framework.request import Request

from applications.locations.models import Location, Pool

class CreatePoolSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Pool
        fields = [
            'name',
            'location',
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
            'pools',
            'created_by',
            'created_at'
        ]

class GetLocationSerializer(serializers.ModelSerializer):

    # pools = CreatePoolSerializer(read_only=True, many=True)
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
            # 'pools',
        ]
    
    def get_full_address(self, location:Location):
        return location.get_address()

class GetAllLocationsSerializer(serializers.ModelSerializer):

    # pools = CreatePoolSerializer(read_only=True, many=True)
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
            # 'pools',
        ]
    
    def get_full_address(self, location:Location):
        return location.get_address()

class UpdateLocationSerializer(serializers.ModelSerializer):

    pools = CreatePoolSerializer(read_only=True, many=True)

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
            'pools'
        ]

class GetLocationToSelectSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Location
        fields = [
            'id',
            'name'
        ]

class PoolSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Pool
        fields = [
            'id',
            'name',
            'location',
            'lanes',
            'width',
            'length',
            'min_depth',
            'max_depth',
            'is_available',
        ]

    def create(self,validated_data):
        request: Request = self.context.get('request')
        print('CREATE REQUEST',request.data)

        pool: Pool = Pool.objects.create(
            name=validated_data['name'],
            location=validated_data['location'],
            lanes=validated_data['lanes'],
            width=validated_data['width'],
            length=validated_data['length'],
            min_depth=validated_data['min_depth'],
            max_depth=validated_data['max_depth'],
            is_available=validated_data['is_available']
        )

        if request and hasattr(request,'user'):
            pool.created_by = request.user
            pool.created_at = datetime.now()

        pool.save()

        return validated_data

    def update(self, instance, validated_data):

        request: Request = self.context.get('request')

        pool: Pool = instance
        
        pool.name = validated_data['name'],
        pool.location = validated_data['location'],
        pool.lanes = validated_data['lanes'],
        pool.width = validated_data['width'],
        pool.length = validated_data['length'],
        pool.min_depth = validated_data['min_depth'],
        pool.max_depth = validated_data['max_depth'],
        pool.is_available = validated_data['is_available']

        if request and hasattr(request,'user'):
            pool.updated_by = request.user
            pool.updated_at = datetime.now()

        pool.save()

        return validated_data