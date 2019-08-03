from django.contrib import admin
from .models import Events, Reservations, Seats


admin.site.register(Events)
admin.site.register(Reservations)
admin.site.register(Seats)
