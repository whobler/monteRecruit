from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers

from .payment_adapter import PaymentGateway, CardError, PaymentError, CurrencyError
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
    # This should be a POST method. It is a GET method only for proof of concept and convenience.
    def get(self, request, seat_ids):
        new_reservation = Reservations()
        new_reservation.save()
        for seat_id in seat_ids.split(','):
            current_seat = Seats.objects.get(id=seat_id)
            current_seat.reservation = new_reservation
            current_seat.save()
        return Response(new_reservation.pk)


class PayView(APIView):
    # This should be a POST method. It is a GET method only for proof of concept and convenience.
    def get(self, request, reservation_id, amount, token, currency):
        try:
            p = PaymentGateway()
            p.charge(amount, token, currency)
        except (CardError, PaymentError, CurrencyError) as e:
            return Response(str(e))  # this should be transformed into a JSON object for consistency
        reservation = Reservations.objects.get(id=reservation_id)
        reservation.is_payed = True
        reservation.save()
        return Response('bbb')
