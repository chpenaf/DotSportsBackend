from rest_framework import serializers

from applications.planning.models import Calendar, Slot
from applications.schedule.models import Schedule_Day
from applications.catalog.models import Course

from applications.catalog.api.serializers import CourseSerializer

from ..models import (
    CourseAssigned,
    CourseSchedule,
    CourseSession
)

class CourseAssignedSerializer(serializers.ModelSerializer):

    schedule = serializers.SerializerMethodField(read_only=True)
    sessions = serializers.SerializerMethodField(read_only=True)
    enddate  = serializers.DateField(read_only=True)

    class Meta:
        model  = CourseAssigned
        fields = [
            'id',
            'location',
            'pool',
            'lane',
            'course',
            'level',
            'num_sessions',
            'teacher',
            'startdate',
            'enddate',
            'schedule',
            'sessions'
        ]

    def get_schedule(self, instance: CourseAssigned):
        schedule: CourseSchedule = CourseSchedule.objects.all().filter(
            course_assigned = instance
        )
        serializer = CourseScheduleSerializer(
            schedule,
            many=True
        )
        return serializer.data
    
    def get_sessions(self, instance: CourseAssigned):
        sessions: CourseSession = CourseSession.objects.all().filter(
            course_assigned = instance
        )
        serializer = CourseSessionSerializer(
            sessions,
            many=True
        )
        return serializer.data

class CourseAssignedSerializer2(serializers.ModelSerializer):

    course = CourseSerializer()

    class Meta:
        model  = CourseAssigned
        fields = [
            'id',
            'location',
            'pool',
            'lane',
            'course',
            'level',
            'num_sessions',
            'teacher',
            'startdate'
        ]

class CourseScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model  = CourseSchedule
        fields = [
            'id',
            'course_assigned',
            'weekday',
            'slot'
        ]

class CourseSessionSerializer(serializers.ModelSerializer):

    lane = serializers.SerializerMethodField(read_only=True)
    desc = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model  = CourseSession
        fields = [
            'id',
            'date',
            'slot',
            'lane',
            'desc'
        ]

    def get_lane(self, instance: CourseSession):

        return instance.course_assigned.lane.lane_no
    
    def get_desc(self, instance: CourseSession):
        
        return '{0} {1}'.format(
            instance.course_assigned.course.name,
            instance.course_assigned.level.name
        )


class SlotSerializer(serializers.Serializer):

    slot = serializers.TimeField()

class WeekSerializer(serializers.Serializer):

    slots = SlotSerializer()