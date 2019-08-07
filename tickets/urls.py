from django.urls import path

from . import views

urlpatterns = [
    path('events/<int:event_id>/', views.EventView.as_view(), name='event_view'),
    path('events/<int:event_id>/available_tickets', views.AvailableTicketsView.as_view(), name='available_tickets_view'),
    path('reserve_ticket/', views.ReserveTicketView.as_view(), name='reserve_ticket_view'),  # POST only
    path('pay/', views.PayView.as_view(), name='pay_view'),  # POST only
    path('reservations/<int:reservation_id>/', views.ReservationView.as_view(), name='reservation_view'),
    path('statistics/<str:statistics_type>/', views.StatisticsView.as_view(), name='statistics_view'),
]