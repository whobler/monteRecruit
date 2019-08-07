from rest_framework import serializers

from .models import Events, Reservations


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['id', 'name', 'datetime']


class ReservationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = ['id', 'is_payed', 'reservation_time']