from datetime import datetime, timezone

from django_cron import CronJobBase, Schedule

from .models import Reservations


class RemoveOutdatedReservations(CronJobBase):
    RUN_EVERY_MINS = 1  # runs every minute

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tickets.remove_invalid_reservations'

    def do(self):
        all_reservations = Reservations.objects.all()
        for reservation in all_reservations:
            if abs((reservation.reservation_time - datetime.now(timezone.utc)).total_seconds()) > 15*60 \
                    and reservation.is_payed is False:
                reservation.delete()
