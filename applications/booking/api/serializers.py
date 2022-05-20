from datetime import datetime

from rest_framework import serializers

from applications.credits.api.serializers import (
    CreditPositionSerializer
)

from applications.planning.api.serializers import (
    SlotSerializer
)

from ..models import Booking

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Booking
        fields = '__all__'

class BookingListSerializer(serializers.ModelSerializer):

    slot = SlotSerializer(read_only=True)
    credit_pos = CreditPositionSerializer(read_only=True)
    old = serializers.SerializerMethodField()

    class Meta:
        model  = Booking
        fields = [
            'member',
            'calendar',
            'slot',
            'location',
            'pool',
            'credit_header',
            'credit_pos',
            'old'
        ]

    def get_old(self, instance: Booking):
        if datetime.now().date() > instance.calendar.date:
            return True
        elif datetime.now().date() == instance.calendar.date and datetime.now().time() > instance.slot.starttime:
            return True
        else:
            return False