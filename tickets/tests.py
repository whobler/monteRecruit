from django.urls import reverse
from rest_framework.test import APITestCase

from .views import NO_EVENT_FOUND_MESSAGE
from .models import Events


some_datetime = "2029-01-03T15:44:46.743Z"


class EventViewTest(APITestCase):
    def setUp(self):
        Events.objects.create(name='testEvent123', datetime=some_datetime)

    def test_event_not_existing(self):
        """Check for behaviour when event does not exist."""
        url = reverse('EventView', kwargs={'event_id': 2})
        response = self.client.get(url, {}, format='json')
        self.assertContains(response, NO_EVENT_FOUND_MESSAGE, status_code=200)

    def test_event_ok(self):
        """Check if endpoint returns proper response when existing event given."""
        event = Events.objects.get(id=1)
        url = reverse('EventView', kwargs={'event_id': 1})
        response = self.client.get(url, {}, format='json')
        expected_data = {
            "event_id": event.id,
            "event_name": event.name,
            "date_time": some_datetime
        }

        assert expected_data == response.json()
        self.assertEqual(response.status_code, 200)


# class AvailableTicketsViewTest(APITestCase):
#     def setUp(self):
#         Events.objects.create(name='testEvent123', datetime=some_datetime)
#
#     def test_available_tickets_ok(self):
#         """Check if endpoint returns proper response when asking for an existing event."""
#
#         url = reverse('ReserveTicketView', kwargs={'event_id': 1})
#         response = self.client.get(url, {}, format='json')
#         self.assertContains(response,  status_code=200)

