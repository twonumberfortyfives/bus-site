from rest_framework import serializers
from station.models import Bus


class BusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    info = serializers.CharField(required=False, max_length=255)
    num_seats = serializers.IntegerField(required=True)

    class Meta:
        model = Bus
        fields = ('id', 'info', 'num_seats')

    def create(self, validated_data):
        """
        Create and return a new `Bus` instance, given the validated data
        """
        return Bus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Bus` instance, given the validated data
        """
        instance.info = validated_data.get('info', instance.info)
        instance.num_seats = validated_data.get('num_seats', instance.num_seats)
        instance.save()
        return instance
