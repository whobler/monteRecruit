from django.urls import path

from . import views

urlpatterns = [
    path('events/<int:event_id>/', views.EventView.as_view(), name='EventView'),
    path('events/<int:event_id>/available_tickets', views.AvailableTicketsView.as_view(), name='AvailableTicketsView'),
    path('reserve_ticket/<str:seat_ids>/', views.ReserveTicketView.as_view(), name='ReserveTicketView'),
    path('pay/<int:reservation_id>/<int:amount>/<str:token>/<str:currency>',
         views.PayView.as_view(), name='PayView'),
    path('reservations/<int:reservation_id>/', views.ReservationView.as_view(), name='ReservationView'),
    path('statistics/<str:statistics_type>/', views.StatisticsView.as_view(), name='StatisticsView'),
]