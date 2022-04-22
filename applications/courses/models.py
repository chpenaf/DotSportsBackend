from django.db import models

from applications.catalog.models import Course, Course_Level
from applications.locations.models import Location, Pool, Lane
from applications.schedule.models import Schedule_Slot
from applications.planning.models import Calendar, Slot

class CourseAssigned(models.Model):

    location = models.ForeignKey(
        Location,
        on_delete=models.DO_NOTHING,
        verbose_name='Sede'
    )

    pool = models.ForeignKey(
        Pool,
        on_delete=models.DO_NOTHING,
        verbose_name='Píscina'
    )

    lane = models.ForeignKey(
        Lane,
        on_delete=models.DO_NOTHING
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Curso'
    )

    level = models.ForeignKey(
        Course_Level,
        on_delete=models.CASCADE,
        verbose_name='Nivel',
        blank=True,
        null=True
    )

    num_sessions = models.IntegerField(
        verbose_name='Cantidad de sesiones'
    )

    teacher = models.CharField(
        verbose_name='Profesor',
        max_length=100,
        blank=True,
        null=True
    )

    startdate = models.DateField(
        verbose_name='Inicio'
    )

    enddate = models.DateField(
        verbose_name='Fin'
    )


    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return '{0} - {1} {2}'.format(
            self.location.name,
            self.course.name,
            self.level.name
        )

class CourseSchedule(models.Model):

    MONDAY    = 1
    TUESDAY   = 2
    WEDNESDAY = 3
    THURSDAY  = 4
    FRIDAY    = 5
    SATURDAY  = 6
    SUNDAY    = 7

    WEEKDAYS_CHOICES = [
        ( MONDAY, 'Lunes' ),
        ( TUESDAY, 'Martes' ),
        ( WEDNESDAY, 'Miércoles' ),
        ( THURSDAY, 'Jueves' ),
        ( FRIDAY, 'Viernes' ),
        ( SATURDAY, 'Sábado' ),
        ( SUNDAY, 'Domingo')
    ]
    
    course_assigned = models.ForeignKey(
        CourseAssigned,
        on_delete=models.CASCADE
    )

    weekday = models.IntegerField(
        verbose_name='Día de la semana',
        choices=WEEKDAYS_CHOICES,
        default=MONDAY
    )

    slot = models.ForeignKey(
        Schedule_Slot,
        on_delete=models.DO_NOTHING,
        verbose_name='Bloque horario (plan)'
    )

    class Meta:
        verbose_name = 'Horario Curso'
        verbose_name_plural = 'Horarios Cursos'

    def __str__(self):
        return 'Curso {0} - {1}: {2}'.format(
            self.course_assigned.course.name,
            self.course_assigned.level.name,
            self.WEEKDAYS_CHOICES[self.weekday - 1][1]
        )

class CourseSession(models.Model):

    course_assigned = models.ForeignKey(
        CourseAssigned,
        on_delete=models.CASCADE
    )

    course_schedule = models.ForeignKey(
        CourseSchedule,
        on_delete=models.CASCADE
    )

    date = models.ForeignKey(
        Calendar, 
        verbose_name='Fecha',
        on_delete=models.CASCADE
    )

    slot = models.ForeignKey(
        Slot,
        verbose_name='Bloque horario',
        on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
    
    def __str__(self):
        return '{0} - {1}: {2} ( {3} - {4} )'.format(
            self.course_assigned.course.name,
            self.course_assigned.level.name,
            self.date,
            self.slot.starttime,
            self.slot.endtime
        )