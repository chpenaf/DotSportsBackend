from rest_framework import serializers

from ..models import Calendar, Slot

class CalendarSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    day = serializers.IntegerField(read_only=True)
    daytype = serializers.CharField(max_length=2, read_only=True)
    day_week = serializers.IntegerField(read_only=True)

    class Meta:
        model  = Calendar
        fields = [
            'id',
            'location',
            'schedule',
            'date',
            'holiday',
            'day',
            'daytype',
            'day_week'
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

class PlanningDaySerializer(serializers.Serializer):

    pass