from rest_framework import serializers

from applications.locations.api.serializers import (
    GetLocationToSelectSerializer,
    PoolSerializerToSelect
)
from ..models import CapacityPool

class CapacityPoolSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model  = CapacityPool
        fields = [
            'id',
            'location',
            'pool',
            'capacity_lane',
            'begin_validity',
            'end_validity'
        ]

class CapacityPoolListSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    location = GetLocationToSelectSerializer()
    pool = PoolSerializerToSelect()

    class Meta:
        model  = CapacityPool
        fields = [
            'id',
            'location',
            'pool',
            'capacity_lane',
            'begin_validity',
            'end_validity'
        ]
