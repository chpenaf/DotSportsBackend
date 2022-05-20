from django.db import models

from applications.credits.models import Credit_Header, Credit_Pos
from applications.locations.models import Location, Pool
from applications.members.models import Member
from applications.planning.models import Calendar, Slot

class Booking(models.Model):

    member = models.ForeignKey(
        Member,
        on_delete=models.DO_NOTHING
    )

    calendar = models.ForeignKey(
        Calendar,
        on_delete=models.DO_NOTHING
    )

    slot = models.ForeignKey(
        Slot,
        on_delete=models.DO_NOTHING
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.DO_NOTHING
    )

    pool = models.ForeignKey(
        Pool,
        on_delete=models.DO_NOTHING
    )

    credit_header = models.ForeignKey(
        Credit_Header,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )

    credit_pos = models.ForeignKey(
        Credit_Pos,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return '{0} {1} {2}'.format(
            self.member.get_short_name(),
            self.calendar.date,
            self.slot.starttime
        )