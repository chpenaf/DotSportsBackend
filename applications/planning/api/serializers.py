from rest_framework import serializers

from ..models import Calendar

class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Calendar
        fields = [
            'location',
            'schedule',
            'date',
            'holiday'
        ]

# class HoliDayAPISerializer(serializers.Serializer):

#     nombre = serializers.CharField(
#         max_length=100,
#         required=False
#     )
#     comentarios = serializers.CharField(
#         max_length=100,
#         required=False
#     )
#     fecha = serializers.DateField(
#         required=False
#     )
#     irrenunciable = serializers.CharField(
#         max_length=1,
#         required=False
#     )
#     tipo = serializers.CharField(
#         max_length=20,
#         required=False
#     )