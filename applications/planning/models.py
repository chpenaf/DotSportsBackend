from datetime import datetime

from django.db import models

from applications.locations.models import Location
from applications.schedule.models import Schedule, Schedule_Day

class Calendar(models.Model):

    MONDAY    = 1
    TUESDAY   = 2
    WEDNESDAY = 3
    THURSDAY  = 4
    FRIDAY    = 5
    SATURDAY  = 6
    SUNDAY    = 7

    JANUARY   = 1
    FEBRUARY  = 2
    MARCH     = 3
    APRIL     = 4
    MAY       = 5
    JUNE      = 6
    JULY      = 7
    AUGUST    = 8
    SEPTEMBER = 9
    OCTOBER   = 10
    NOVEMBER  = 11
    DECEMBER  = 12

    WEEK_CHOICES = [
        ( MONDAY, 'Lunes' ),
        ( TUESDAY, 'Martes' ),
        ( WEDNESDAY, 'Miércoles' ),
        ( THURSDAY, 'Jueves' ),
        ( FRIDAY, 'Viernes' ),
        ( SATURDAY, 'Sábado' ),
        ( SUNDAY, 'Domingo' )
    ]

    MONTHS_CHOICES = [
        ( JANUARY, 'Enero' ),
        ( FEBRUARY, 'Febrero' ),
        ( MARCH, 'Marzo' ),
        ( APRIL, 'Abril' ),
        ( MAY, 'Mayo' ),
        ( JUNE, 'Junio' ),
        ( JULY, 'Julio' ),
        ( AUGUST, 'Agosto' ),
        ( SEPTEMBER, 'Septiembre' ),
        ( OCTOBER, 'Octubre' ),
        ( NOVEMBER, 'Noviembre' ),
        ( DECEMBER, 'Diciembre' ),
    ]

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )

    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.DO_NOTHING
    )

    date = models.DateField(
        verbose_name='Fecha',
        null=False
    )

    year = models.IntegerField(
        verbose_name='Año',
        null=False,
        default=datetime.today().year
    )

    month = models.IntegerField(
        verbose_name='Mes',
        null=False,
        default=datetime.today().month
    )

    day = models.IntegerField(
        verbose_name='Día',
        null=False,
        default=datetime.today().day
    )

    daytype = models.CharField(
        max_length=2,
        choices=Schedule_Day.DAYS_CHOICES,
        default=Schedule_Day.WEEKDAY
    )

    day_week = models.IntegerField(
        verbose_name='Día de la semana',
        null=False,
        default=datetime.today().weekday() + 1
    )

    day_label = models.CharField(
        verbose_name='Nombre día',
        max_length=10,
        choices=WEEK_CHOICES,
        default=WEEK_CHOICES[datetime.today().weekday()]
    )

    month_label = models.CharField(
        verbose_name='Nombre mes',
        max_length=10,
        choices=MONTHS_CHOICES,
        default=MONTHS_CHOICES[datetime.today().month - 1]
    )

    holiday = models.BooleanField(
        verbose_name='Feriado',
        null=True,
        blank=True,
        default=False
    )

    class Meta:
        verbose_name='Calendario'
        verbose_name_plural='Calendarios'
        unique_together=['location','date']

    def __str__(self):
        return '{0}-{1}-{2}'.format(
            self.day,
            self.month,
            self.year
        )
    
    def get_date(self):
        return datetime(self.year,self.month,self.day).date()