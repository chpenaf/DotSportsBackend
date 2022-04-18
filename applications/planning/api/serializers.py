from rest_framework import serializers

from ..models import Calendar, Slot

class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Calendar
        fields = [
            'location',
            'schedule',
            'date',
            'holiday'
        ]

class SlotSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Slot
        fields = [
            'id',
            'calendar',
            'slot',
            'starttime',
            'endtime'
        ]