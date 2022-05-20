from dataclasses import field
from rest_framework import serializers

from ..models import Booking

class BookingSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    credit_header = serializers.IntegerField(read_only=True)
    credit_pos = serializers.IntegerField(read_only=True)

    class Meta:
        model  = Booking
        fields = [
            'id',
            'member',
            'calendar',
            'slot',
            'location',
            'pool',
            'credit_header',
            'credit_pos'
        ]