from django.db import models

from applications.locations.models import Location

class Schedule(models.Model):

    id = models.BigAutoField(
        primary_key=True,
        verbose_name='Id Horario'
    )

    location = models.ForeignKey(
        Location,
        verbose_name='Sede',
        null=False,
        on_delete=models.CASCADE
    )

    begin_validity = models.DateField(
        verbose_name='Inicio de vigencia'
    )

    end_validity = models.DateField(
        verbose_name='Fin vigencia'
    )

    class Meta:
        verbose_name='Horario'
        verbose_name_plural='Horarios'

    def __str__(self):
        return '{0} - {1}'.format(self.id, self.location)

class Schedule_Day(models.Model):

    WEEKDAY  = 'WD'
    SATURDAY = 'SA'
    SUNDAY   = 'SU'
    HOLIDAY  = 'HO'

    DAYS_CHOICES = [
        ( WEEKDAY, 'Lunes a Viernes' ),
        ( SATURDAY, 'Sábado' ),
        ( SUNDAY, 'Domingo' ),
        ( HOLIDAY, 'Festivo' )
    ]

    schedule = models.ForeignKey(
        Schedule,
        related_name='day_type',
        verbose_name='Id Horario',
        on_delete=models.CASCADE
    )

    daytype = models.CharField(
        verbose_name='Tipo de Día',
        max_length=2,
        choices=DAYS_CHOICES,
        default=WEEKDAY
    )

    is_open = models.BooleanField(
        verbose_name='¿Está abierto?',
        default=False
    )

    class Meta:
        verbose_name='Día horario'
        verbose_name_plural='Días horario'
        unique_together = ['schedule','daytype']

    def __str__(self):
        return '{0} - {1}'.format(self.schedule, self.daytype)
    
    def get_daytype(self,weekday: int):

        if weekday >= 1 and weekday <= 5:
            return self.WEEKDAY
        elif weekday == 6:
            return self.SATURDAY
        elif weekday == 7:
            return self.SUNDAY


class Schedule_Slot(models.Model):

    schedule_day = models.ForeignKey(
        Schedule_Day,
        related_name='timeslot',
        verbose_name='Día',
        on_delete=models.CASCADE
    )

    slot = models.IntegerField(
        verbose_name='Slot'
    )

    starttime = models.TimeField(
        verbose_name='Hora Inicio'
    )

    endtime = models.TimeField(
        verbose_name='Hora Fin'
    )

    class Meta:
        verbose_name = 'Bloque horario'
        verbose_name_plural = 'Bloques horario'
        unique_together = ['schedule_day','slot']
        ordering = ['slot']

    def __str__(self):
        return '{0} : {1} - {2}'.format(
            self.schedule_day, 
            self.starttime,
            self.endtime
        )

