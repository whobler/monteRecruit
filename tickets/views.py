from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers

from .models import Events, Seats, Reservations


class EventView(APIView):
    def get(self, request, event_id):
        event = Events.objects.filter(pk=event_id)
        return Response(serializers.serialize('json', event))


class AvailableTicketsView(APIView):
    def get(self, request, event_id):
        available_tickets = Seats.objects.filter(reservation=None)
        return Response(serializers.serialize('json', available_tickets))


class ReserveTicketView(APIView):
    # This should be a POST method. It is a GET method only for proof of concept.
    def get(self, request, seat_ids):
        new_reservation = Reservations()
        new_reservation.save()
        for seat_id in seat_ids.split(','):
            current_seat = Seats.objects.get(id=seat_id)
            current_seat.reservation = new_reservation
            current_seat.save()
        return Response(new_reservation.pk)


class PayView(APIView):
    def get(self, request, reservation_id):
        return Response('bbb')