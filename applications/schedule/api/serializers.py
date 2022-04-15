from urllib.request import Request
from xmlrpc.client import DateTime
from rest_framework import serializers

from ...locations.models import Location
from ...locations.api.serializers import GetLocationToSelectSerializer

from ..models import (
    Schedule, 
    Schedule_Day, 
    Schedule_Slot
)

class ScheduleSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Schedule_Slot
        fields = [
            'slot',
            'starttime',
            'endtime'
        ]

class ScheduleDaySerializer(serializers.ModelSerializer):

    desc = serializers.SerializerMethodField()
    slots = serializers.SerializerMethodField()

    class Meta:
        model  = Schedule_Day
        fields = [
            'daytype',
            'desc',
            'is_open',
            'slots'
        ]
    
    def get_desc(self, instance):
        for item in Schedule_Day.DAYS_CHOICES:
            if item[0] == instance.daytype:
                return item[1]          

    def get_slots(self, instance):
        slots = Schedule_Slot.objects.all().filter(schedule_day=instance)
        serializer = ScheduleSlotSerializer(slots, many=True)
        return serializer.data

class ListScheduleSerializer(serializers.ModelSerializer):

    location = GetLocationToSelectSerializer(
        read_only=True, 
        many=False
    )

    days = serializers.SerializerMethodField()

    class Meta:
        model  = Schedule
        fields = [
            'id',
            'location',
            'begin_validity',
            'end_validity',
            'days'
        ]
    
    def get_days(self,instance):
        days = Schedule_Day.objects.all().filter(schedule=instance)
        serializer = ScheduleDaySerializer(days, many=True)
        return serializer.data

class ScheduleSerializer(serializers.ModelSerializer):

    location_origin = GetLocationToSelectSerializer(
        read_only=True, 
        many=False
    )

    location = serializers.PrimaryKeyRelatedField(
        source="location_origin",
        queryset=Location.objects.all(),
        write_only=True
    )

    class Meta:
        model  = Schedule
        fields = [
            'id',
            'location',
            'location_origin',
            'begin_validity',
            'end_validity'
        ]
    

    def create(self, validated_data):

        schedule: Schedule = Schedule.objects.create(
            location=validated_data['location_origin'],
            begin_validity=validated_data['begin_validity'],
            end_validity=validated_data['end_validity']
        )

        schedule.save()
        serializer = ListScheduleSerializer(
            Schedule.objects.all().filter(id = schedule.id ).first()
        )
        return serializer.data

class CreateScheduleDaySerializer(serializers.ModelSerializer):

    class Meta:
        model  = Schedule_Day
        fields = [
            'schedule',
            'daytype',
            'is_open'
        ]
    
    def create(self, validated_data):
        day: Schedule_Day = Schedule_Day.objects.create(
            schedule=validated_data['schedule'],
            daytype=validated_data['daytype'],
            is_open=validated_data['is_open']
        )
        day.save()
        return {
            'id':day.id,
            'schedule':day.schedule,
            'daytype':day.daytype,
            'is_open':day.is_open
        }

class CreateSlotSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Schedule_Slot
        fields = [
            'schedule_day',
            'slot',
            'starttime',
            'endtime'
        ]

    def create(self, validated_data):
        print(validated_data)
        slot: Schedule_Slot = Schedule_Slot.objects.create(
            schedule_day=validated_data['schedule_day'],
            slot=validated_data['slot'],
            starttime=validated_data['starttime'],
            endtime=validated_data['endtime']
        )
        slot.save()
        return validated_data