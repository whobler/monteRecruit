from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('events/<int:event_id>/', views.EventView.as_view(), name='EventView'),
    path('events/<int:event_id>/available_tickets', views.AvailableTicketsView.as_view(), name='AvailableTicketsView'),
    path('reserve_ticket/<str:seat_ids>/', views.ReserveTicketView.as_view(), name='ReserveTicketView'),
    path('pay/<int:reservation_id>/<int:amount>/<str:token>/<str:currency>',
         views.PayView.as_view(), name='PayView'),

    # # ex: /polls/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]