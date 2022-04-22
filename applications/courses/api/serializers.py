from rest_framework import serializers

from ..models import (
    CourseAsigned,
    CourseSchedule,
    CourseSession
)

class CourseAsignedSerializer(serializers.ModelSerializer):

    class Meta:
        model  = CourseAsigned
        fields = [
            'id',
            'location',
            'pool',
            'lane',
            'course',
            'level',
            'startdate',
            'enddate',
            'teacher'
        ]

class CourseScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model  = CourseSchedule
        fields = [
            'id',
            'course_asigned',
            'weekday',
            'starttime',
            'endtime'
        ]

class CourseSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model  = CourseSession
        fields = [
            'id',
            'course_asigned',
            'date',
            'starttime',
            'endtime'
        ]