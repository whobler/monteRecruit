from django.http import JsonResponse
from rest_framework.views import APIView

from .serializers import EventsSerializer, ReservationsSerializer
from .payment_adapter import PaymentGateway, CardError, PaymentError, CurrencyError
from .models import Events, Seats, Reservations


NO_EVENT_FOUND_MESSAGE = 'No event found.'
NO_TICKET_FOUND_MESSAGE = 'One or more tickets do not exist.'
NO_RESERVATION_FOUND_MESSAGE = 'No reservation found.'
NO_TICKETS_FOR_EVENT_MESSAGE = "No available tickets found for this event."
TICKET_ALREADY_RESERVED_MESSAGE = 'One or more tickets already reserved.'
RESERVATION_ALREADY_PAID_MESSAGE = "Reservation already paid for."
PAYMENT_SUCCESSFUL_MESSAGE = 'Payment for reservation {} successful.'


class EventView(APIView):
    def get(self, request, event_id):
        """Endpoint for getting more detailed information about a single event."""
        event = Events.objects.filter(pk=event_id).first()
        if event:
            data = EventsSerializer(event).data
        else:
            data = {'info': NO_EVENT_FOUND_MESSAGE}
        return JsonResponse(data)


class AvailableTicketsView(APIView):
    def get(self, request, event_id):
        """Endpoint for checking all available(not reserved) tickets for a single event."""
        event = Events.objects.filter(pk=event_id).first()
        if event:
            available_tickets = Seats.objects.filter(reservation=None, event=event)
            if available_tickets:
                data = {
                    'available_tickets': [{'ticket_id': s.id, 'ticket_type': s.type} for s in available_tickets]
                }
            else:
                data = {'info': NO_TICKETS_FOR_EVENT_MESSAGE}
        else:
            data = {'info': NO_EVENT_FOUND_MESSAGE}
        return JsonResponse(data)


class ReserveTicketView(APIView):
    def post(self, request):
        """Endpoint for reserving ticket(s). Multiple tickets can be reserved at once."""
        new_reservation = Reservations()
        new_reservation.save()
        seat_ids = request.data['seat_ids']
        for seat_id in seat_ids.split(','):
            current_seat = Seats.objects.filter(id=seat_id).first()
            if not current_seat:
                return JsonResponse({'error': NO_TICKET_FOUND_MESSAGE})
            if current_seat.reservation is None:
                current_seat.reservation = new_reservation
                current_seat.save()
            else:
                return JsonResponse({'error': TICKET_ALREADY_RESERVED_MESSAGE})
        return JsonResponse({'new_reservation_id': new_reservation.pk})


class PayView(APIView):
    # This should be a POST method. It is a GET method only for proof of concept and convenience.
    def get(self, request, reservation_id, amount, token, currency):
        """
        Endpoint for payment purposes.
        Notes:
            -'amount' can be any integer number (probably should a float in a completed application)
            -'token' can be almost anything (see payment_adapter.py for details)
            -'currency' can be only 'EUR' at the moment (see payment_adapter.py for details)
            anything else will resolve in an error (most of them are caught).

        Also, there is probably a better way to send these information to this endpoint.
        In the URL it does not seem secure. Pardon my Django incompetence :)
        """
        reservation = Reservations.objects.get(id=reservation_id)
        if reservation:
            if reservation.is_payed is True:
                data = {'error': RESERVATION_ALREADY_PAID_MESSAGE}
            else:
                try:
                    pg = PaymentGateway()
                    pg.charge(amount, token, currency)
                except (CardError, PaymentError, CurrencyError) as e:
                    return JsonResponse({'errors': str(e)})
                reservation.is_payed = True
                reservation.save()
                data = {'info': PAYMENT_SUCCESSFUL_MESSAGE.format(reservation_id)}
        else:
            data = {'error': NO_RESERVATION_FOUND_MESSAGE}
        return JsonResponse(data)


class ReservationView(APIView):
    def get(self, request, reservation_id):
        """Endpoint for getting detailed information about a single reservation."""
        reservation = Reservations.objects.filter(id=reservation_id).first()
        if reservation:
            reserved_seats = Seats.objects.filter(reservation=reservation)
            seat_ids = [seat.id for seat in reserved_seats]
            data = ReservationsSerializer(reservation).data
            data['reserved_seats'] = seat_ids
        else:
            data = {'errors': NO_RESERVATION_FOUND_MESSAGE}
        return JsonResponse(data)


class StatisticsView(APIView):
    def get(self, request, statistics_type):
        """
        Endpoint for getting statistics.
        Currently implemented statistics:
        -reserved_tickets_per_event returns amount of reserved tickets per event
        -reserved_tickets_by_type returns amount of reserved tickets per type
        """
        data = {}
        if statistics_type == "reserved_tickets_per_event":
            for event in Events.objects.all():
                data[event.name] = event.seats_set.filter(reservation__isnull=False).count()
        elif statistics_type == "reserved_tickets_by_type":
            for seat_type in Seats.SEATS_TYPE_CHOICES:
                data[seat_type[1]] = Seats.objects.filter(type=seat_type[0], reservation__isnull=False).count()
        return JsonResponse(data)

        # statistic idea: histogram of how many reservations were made per day
