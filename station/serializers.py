from rest_framework import serializers
from station.models import Bus, Trip, Ticket, Facility


# class BusSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     info = serializers.CharField(required=False, max_length=255)
#     num_seats = serializers.IntegerField(required=True)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Bus` instance, given the validated data
#         """
#         return Bus.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Bus` instance, given the validated data
#         """
#         instance.info = validated_data.get('info', instance.info)
#         instance.num_seats = validated_data.get('num_seats', instance.num_seats)
#         instance.save()
#         return instance

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ("id", "name")


class BusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bus
        fields = ("id", "info", "num_seats", "is_small", "facilities")


class BusListSerializer(BusSerializer):
    facilities = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )


class BusRetrieveSerializer(BusSerializer):
    facilities = FacilitySerializer(many=True, read_only=True)


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ("id", "source", "destination", "departure", "bus")


class TripListSerializer(TripSerializer):
    bus = BusSerializer(read_only=True)


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "seat", "trip", "order")
