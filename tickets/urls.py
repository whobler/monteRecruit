from django.urls import path

from . import views

urlpatterns = [
    path('events/<int:event_id>/', views.EventView.as_view(), name='event_view'),
    path('events/<int:event_id>/available_tickets', views.AvailableTicketsView.as_view(), name='available_tickets_view'),
    path('reserve_ticket/<str:seat_ids>/', views.ReserveTicketView.as_view(), name='reserve_ticket_view'),
    path('pay/<int:reservation_id>/<int:amount>/<str:token>/<str:currency>',
         views.PayView.as_view(), name='pay_view'),
    path('reservations/<int:reservation_id>/', views.ReservationView.as_view(), name='reservation_view'),
    path('statistics/<str:statistics_type>/', views.StatisticsView.as_view(), name='statistics_view'),
]