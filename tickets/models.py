from django.db import models


class Events(models.Model):
    """Events model."""
    name = models.CharField(max_length=90, null=False)
    datetime = models.DateTimeField(auto_now=True)


class Reservations(models.Model):
    """Reservations model. There can be multiple Reservations for an Event."""
    is_payed = models.BooleanField(default=False)
    reservation_time = models.DateTimeField(auto_now=True)


class Seats(models.Model):
    """Seats model. There can be multiple Seats for each Event. A Reservation can reference many Seats."""
    REGULAR = 'Regular'
    PREMIUM = 'Premium'
    VIP = 'VIP'
    SEATS_TYPE_CHOICES = [REGULAR, PREMIUM, VIP]
    type = models.CharField(choices=SEATS_TYPE_CHOICES, default=REGULAR, null=False)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=False)
    reservation = models.ForeignKey(Reservations, on_delete=models.CASCADE)
