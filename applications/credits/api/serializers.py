from rest_framework import serializers

from ..models import Credit_Header, Credit_Pos

class CreditHeaderSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(
        required=False
    )

    status = serializers.CharField(
        max_length=2,
        required=False
    )

    end_validity = serializers.DateField(
        required=False
    )

    positions = serializers.SerializerMethodField()

    class Meta:
        model  = Credit_Header
        fields = [
            'id',
            'location',
            'member',
            'quantity',
            'status',
            'begin_validity',
            'end_validity',
            'entered_by',
            'doc_ref',
            'positions'
        ]
    
    def get_positions(self, instance):
        positions = Credit_Pos.objects.all().filter(header=instance)
        serializer = CreditPositionSerializer(positions, many=True)
        return serializer.data

class CreditPositionSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(
        required=False
    )

    class Meta:
        model  = Credit_Pos
        fields = [
            'id',
            'pos',
            'begin_validity',
            'end_validity',
            'status',
            'used_at'
        ]