from rest_framework import serializers
from applications.courses.models import CourseAssigned, CourseSession

from applications.locations.models import Pool, Lane
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

class PlanningLaneSerializer(serializers.ModelSerializer):

    desc = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model  = Lane
        fields = [
            'id',
            'lane_no',
            'desc'
        ]

    def get_desc(self, instance: Lane):
        slot: Slot = self.context.get('slot')

        course_assigned: CourseAssigned = CourseAssigned.objects.filter(
            lane=instance
        ).first()

        if course_assigned:

            session: CourseSession = CourseSession.objects.filter(
                course_assigned=course_assigned,
                slot=slot
            ).first()

            if session:
                return '{0} {1}'.format(
                    session.course_assigned.course.name,
                    session.course_assigned.level.name
                )
            else:
                return 'Nado Libre'
        
        else:
            return 'Nado Libre'


class PlanningDaySerializer(serializers.ModelSerializer):

    lanes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model  = Slot
        fields = [
            'id',
            'calendar',
            'slot',
            'starttime',
            'endtime',
            'lanes'
        ]
    
    def get_lanes(self, instance: Slot):

        pool: Pool = self.context.get('pool')

        serializer = PlanningLaneSerializer(
            Lane.objects.all().filter( id_pool = pool ),
            context={'slot': instance},
            many=True
        )

        return serializer.data