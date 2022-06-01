from rest_framework import serializers

from applications.locations.api.serializers import GetLocationToSelectSerializer

from ..models import (
    Service,
    Catalog,
    Course,
    Service_Subcategory,
    Course_Level
)

class ServiceSerializer(serializers.ModelSerializer):

    subcategories = serializers.SerializerMethodField()

    class Meta:
        model  = Service
        fields = [
            'id',
            'name',
            'subcategories'
        ]
    
    def get_subcategories(self, instance):
        serializer = ServiceSubcategorySerializer(
            Service_Subcategory.objects.all().filter(service=instance),
            many=True
        )
        return serializer.data

class ServiceSubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model  = Service_Subcategory
        fields = [
            'id',
            'service',
            'level',
            'name'
        ]

class CourseLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model  = Course_Level
        fields = [
            'id',
            'course',
            'name',
            'level'
        ]

class CourseSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    levels = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model  = Course
        fields = [
            'id',
            'name',
            'levels'
        ]

    def get_levels(self, instance):
        serializer = CourseLevelSerializer(
            Course_Level.objects.all().filter(course=instance),
            many=True
        )
        return serializer.data

class CatalogSerializer(serializers.ModelSerializer):

    location = GetLocationToSelectSerializer(many=False)
    services = ServiceSerializer(many=True)
    courses = CourseSerializer(many=True)

    class Meta:
        model  = Catalog
        fields = [
            'location',
            'services',
            'courses'
        ]