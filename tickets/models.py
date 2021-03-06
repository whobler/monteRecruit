from django.db import models


class Events(models.Model):
    """Events model."""
    name = models.CharField(max_length=90, null=False)
    datetime = models.DateTimeField(null=False)

    def __str__(self):
        return self.name


class Reservations(models.Model):
    """Reservations model. There can be multiple Reservations for an Event. A Reservation can reference many Seats."""
    is_payed = models.BooleanField(default=False)
    reservation_time = models.DateTimeField(auto_now=True)


class Seats(models.Model):
    """Seats model. There can be multiple Seats for each Event."""
    SEATS_TYPE_CHOICES = [
        (1, 'Regular'),
        (2, 'Premium'),
        (3, 'VIP')
    ]  # this could be moved into a separate model for easier management of seat types
    type = models.CharField(choices=SEATS_TYPE_CHOICES, max_length=3, default=1, null=False)
    event = models.ForeignKey(Events, on_delete=models.CASCADE, null=False)
    reservation = models.ForeignKey(Reservations, on_delete=models.CASCADE, null=True, blank=True)
    # in full working app there would be probably a PRICE somewhere here
