from django.urls import reverse
from rest_framework.test import APITestCase

from .views import (
    NO_EVENT_FOUND_MESSAGE,
    NO_TICKETS_FOR_EVENT_MESSAGE,
    TICKET_ALREADY_RESERVED_MESSAGE,
    NO_TICKET_FOUND_MESSAGE,
    PAYMENT_SUCCESSFUL_MESSAGE,
    RESERVATION_ALREADY_PAID_MESSAGE, NO_RESERVATION_FOUND_MESSAGE)
from .models import Events, Reservations, Seats


some_datetime = "2029-01-03T15:44:46.743000Z"
event_name = 'testEvent123'


class EventViewTest(APITestCase):
    def setUp(self):
        Events.objects.create(name=event_name, datetime=some_datetime)

    def test_event_not_existing(self):
        """Check for behaviour when event does not exist."""
        url = reverse('event_view', kwargs={'event_id': 2})
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'info': NO_EVENT_FOUND_MESSAGE}, response.json())

    def test_ok(self):
        """Check if endpoint behaves properly with proper data."""
        event = Events.objects.get(id=1)
        url = reverse('event_view', kwargs={'event_id': 1})
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, 200)
        expected_response = {
            "id": event.id,
            "name": event.name,
            "datetime": some_datetime
        }
        self.assertEqual(expected_response, response.json())


class AvailableTicketsViewTest(APITestCase):
    def setUp(self):
        Events.objects.create(name=event_name, datetime=some_datetime)

    def test_ok(self):
        """Check if endpoint behaves properly with proper data."""
        event = Events.objects.get(id=1)
        Seats.objects.create(type=1, event=event)
        url = reverse('available_tickets_view', kwargs={'event_id': 1})
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, 200)
        expected_response = {'available_tickets': [{'ticket_id': 1, 'ticket_type': '1'}]}
        self.assertEqual(expected_response, response.json())

    def test_event_not_existing(self):
        """Check for behaviour when event does not exist."""
        url = reverse('available_tickets_view', kwargs={'event_id': 2})
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual({'info': NO_EVENT_FOUND_MESSAGE}, response.json())

    def test_returning_only_not_reserved_tickets(self):
        """Check for behaviour when there are only reserved tickets."""
        url = reverse('available_tickets_view', kwargs={'event_id': 1})
        event = Events.objects.get(id=1)
        reservation = Reservations.objects.create()
        Seats.objects.create(type=1, event=event, reservation=reservation)
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual({'info': NO_TICKETS_FOR_EVENT_MESSAGE}, response.json())


class ReserveTicketViewTest(APITestCase):
    url = reverse('reserve_ticket_view')

    def setUp(self):
        event = Events.objects.create(name=event_name, datetime=some_datetime)
        Seats.objects.create(type=1, event=event)
        Seats.objects.create(type=3, event=event)

    def test_ok(self):
        """Check if endpoint behaves properly with proper data."""
        response = self.client.post(self.url, {'seat_ids': "2,1"}, format='json')

        self.assertEqual(response.status_code, 200)
        expected_response = {'new_reservation_id': 1}
        self.assertEqual(expected_response, response.json())
        self.assertEqual(Reservations.objects.all().count(), 1)

    def test_already_reserved(self):
        """Check if tickets do not get reserved if one is already reserved."""
        seat_1 = Seats.objects.get(id=1)
        reservation = Reservations.objects.create()
        seat_1.reservation = reservation
        seat_1.save()
        response = self.client.post(self.url, {'seat_ids': "1,2"}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual({'errors': TICKET_ALREADY_RESERVED_MESSAGE}, response.json())
        self.assertEqual(Seats.objects.get(id=2).reservation, None)

    def test_ticket_not_existing(self):
        """Check if endpoint returns proper response when not existing tickets given"""
        response = self.client.post(self.url, {'seat_ids': "10,15"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'errors': NO_TICKET_FOUND_MESSAGE}, response.json())


class PayViewTest(APITestCase):
    url = reverse('pay_view')

    def setUp(self):
        event = Events.objects.create(name=event_name, datetime=some_datetime)
        reservation = Reservations.objects.create()
        Seats.objects.create(type=1, event=event, reservation=reservation)

    def test_ok(self):
        """Check if endpoint behaves properly with proper data."""
        data = {
            'reservation_id': 1,
            'amount': 10.7,
            'currency': 'EUR',
            'token': 'testing_token'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, 200)
        expected_response = {'info': PAYMENT_SUCCESSFUL_MESSAGE.format(1)}
        self.assertEqual(expected_response, response.json())
        self.assertEqual(Reservations.objects.get(id=1).is_payed, True)

    def test_reservation_already_payed(self):
        """Check if endpoint returns proper response when reservation is already paid for."""
        reservation = Reservations.objects.get(id=1)
        reservation.is_payed = True
        reservation.save()
        data = {
            'reservation_id': 1,
            'amount': 10.7,
            'currency': 'EUR',
            'token': 'testing_token'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual({'errors': RESERVATION_ALREADY_PAID_MESSAGE}, response.json())

    def test_reservation_not_existing(self):
        """Check if endpoint returns proper response when reservation does not exist."""
        data = {
            'reservation_id': 665,
            'amount': 10.7,
            'currency': 'EUR',
            'token': 'testing_token'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual({'errors': NO_RESERVATION_FOUND_MESSAGE}, response.json())

    def test_invalid_currency(self):
        """Check if endpoint returns proper response when invalid currency given."""
        data = {
            'reservation_id': 1,
            'amount': 10.7,
            'currency': '$',
            'token': 'testing_token'
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual({'errors': 'Currency $ not supported'}, response.json())

    def test_invalid_token(self):
        """Check if endpoint returns proper response when invalid token given."""
        data = {
            'reservation_id': 1,
            'amount': 10.7,
            'currency': 'EUR',
            'token': 'card_error'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'errors': 'Your card has been declined'}, response.json())

        data['token'] = 'payment_error'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({'errors': 'Something went wrong with your transaction'}, response.json())

