from django.urls import reverse
from rest_framework.test import APITestCase

from .views import NO_EVENT_FOUND_MESSAGE, NO_TICKETS_FOR_EVENT_MESSAGE
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
        self.assertContains(response, NO_EVENT_FOUND_MESSAGE, status_code=200)

    def test_ok(self):
        """Check if endpoint returns proper response when existing event given."""
        event = Events.objects.get(id=1)
        url = reverse('event_view', kwargs={'event_id': 1})
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, 200)
        expected_response = {
            "id": event.id,
            "name": event.name,
            "datetime": some_datetime
        }
        assert expected_response == response.json()


class AvailableTicketsViewTest(APITestCase):
    def setUp(self):
        Events.objects.create(name=event_name, datetime=some_datetime)

    def test_ok(self):
        """Check if endpoint returns proper response when asking for an existing event."""
        event = Events.objects.get(id=1)
        Seats.objects.create(type=1, event=event)
        url = reverse('available_tickets_view', kwargs={'event_id': 1})
        response = self.client.get(url, {}, format='json')

        self.assertEqual(response.status_code, 200)
        expected_response = {'available_tickets': [{'ticket_id': 1, 'ticket_type': '1'}]}
        assert expected_response == response.json()

    def test_event_not_existing(self):
        """Check for behaviour when event does not exist."""
        url = reverse('available_tickets_view', kwargs={'event_id': 2})
        response = self.client.get(url, {}, format='json')

        self.assertContains(response, NO_EVENT_FOUND_MESSAGE, status_code=200)

    def test_returning_only_not_reserved_tickets(self):
        """Check for behaviour when there are only reserved tickets."""
        url = reverse('available_tickets_view', kwargs={'event_id': 1})
        event = Events.objects.get(id=1)
        reservation = Reservations.objects.create()
        Seats.objects.create(type=1, event=event, reservation=reservation)
        response = self.client.get(url, {}, format='json')

        self.assertContains(response, NO_TICKETS_FOR_EVENT_MESSAGE, status_code=200)


class ReserveTicketViewTest(APITestCase):
    def setUp(self):
        event = Events.objects.create(name=event_name, datetime=some_datetime)
        Seats.objects.create(type=1, event=event)
        Seats.objects.create(type=3, event=event)

    def test_ok(self):
        """Check if endpoint returns proper response."""
        url = reverse('reserve_ticket_view')
        response = self.client.post(url, {'seat_ids': "2,1"}, format='json')

        self.assertEqual(response.status_code, 200)
        expected_response = {'new_reservation_id': 1}
        assert expected_response == response.json()
        self.assertEqual(Reservations.objects.all().count(), 1)

    # def test_already_reserved(self):
    #     """Check if tickets do not get reserved if is already reserved."""
    #     url = reverse('reserve_ticket_view', kwargs={'seat_ids': "2,1"})
    #     response = self.client.get(url, {}, format='json')
