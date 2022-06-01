from datetime import datetime

from rest_framework import serializers

from applications.credits.api.serializers import (
    CreditPositionSerializer
)

from applications.members.api.serializers import (
    RetrieveSerializer
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
            'id',
            'member',
            'calendar',
            'slot',
            'location',
            'pool',
            'credit_header',
            'credit_pos',
            'old'
        ]

    def to_representation(self, instance: Booking):
        return {
            'id': instance.id,
            'member': instance.member.id,
            'calendar': instance.calendar.id,
            'slot': SlotSerializer(instance.slot).data,
            'location': instance.location.name,
            'pool': instance.pool.name,
            'credit_header': instance.credit_header.id,
            'credit_pos': CreditPositionSerializer(instance.credit_pos).data,
            'old': self.get_old(instance)
        }
    
    def get_old(self, instance: Booking):
        if datetime.now().date() > instance.calendar.date:
            return True
        elif datetime.now().date() == instance.calendar.date and datetime.now().time() > instance.slot.starttime:
            return True
        else:
            return False

class MemberBySlotSerializer(serializers.ModelSerializer):

    member = RetrieveSerializer()

    class Meta:
        model  = Booking
        fields = [
            'id',
            'member'
        ]