from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .payment_adapter import PaymentGateway, CardError, PaymentError, CurrencyError
from .models import Events, Seats, Reservations


NO_EVENT_FOUND_MESSAGE = "No event found."
NO_TICKETS_FOR_EVENT_MESSAGE = "No available tickets found for this event."
NO_TICKET_FOUND_MESSAGE = 'One or more tickets do not exist'
TICKET_ALREADY_RESERVED_MESSAGE = 'One or more tickets already reserved.'


class EventView(APIView):
    def get(self, request, event_id):
        event = Events.objects.filter(pk=event_id).first()
        if event:
            data = {
                'event_id': event.id,
                'event_name': event.name,
                'date_time': event.datetime
            }
        else:
            data = {'info': NO_EVENT_FOUND_MESSAGE}
        return JsonResponse(data)


class AvailableTicketsView(APIView):
    def get(self, request, event_id):
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
    # This should be a POST method. It is a GET method only for proof of concept and convenience.
    def get(self, request, seat_ids):
        new_reservation = Reservations()
        new_reservation.save()
        for seat_id in seat_ids.split(','):
            current_seat = Seats.objects.get(id=seat_id)
            if not current_seat:
                return JsonResponse({'error': NO_TICKET_FOUND_MESSAGE})
            if current_seat.reservation is None:
                current_seat.reservation = new_reservation
                current_seat.save()
            else:
                return JsonResponse({'error': TICKET_ALREADY_RESERVED_MESSAGE})
        return JsonResponse({'new_reservation': new_reservation.pk})


class PayView(APIView):
    # This should be a POST method. It is a GET method only for proof of concept and convenience.
    def get(self, request, reservation_id, amount, token, currency):
        try:
            pg = PaymentGateway()
            pg.charge(amount, token, currency)
        except (CardError, PaymentError, CurrencyError) as e:
            return Response(str(e))
        reservation = Reservations.objects.get(id=reservation_id)
        reservation.is_payed = True
        reservation.save()
        return Response(reservation.pk)


class ReservationView(APIView):
    def get(self, request, reservation_id):
        reservation = Reservations.objects.filter(id=reservation_id).first()
        if reservation:
            reserved_seats = Seats.objects.filter(reservation=reservation)
            seat_ids = [seat.id for seat in reserved_seats]
            data = {
                'reservation_id': reservation.pk,
                'reservation_time': reservation.reservation_time,
                'is_payed': reservation.is_payed,
                'reserved_seats': seat_ids,
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'errors': "No reservation found."})
