from datetime import datetime

from django.db import models

from applications.catalog.models import Course, Course_Level
from applications.locations.models import Location, Pool, Lane
from applications.planning.models import Calendar

class CourseAsigned(models.Model):

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

    startdate = models.DateField(
        verbose_name='Inicio',
        default=datetime.today().date()
    )

    enddate = models.DateField(
        verbose_name='Fin',
        default=datetime.today().date()
    )

    teacher = models.CharField(
        verbose_name='Profesor',
        max_length=100,
        blank=True,
        null=True
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
    
    course_asigned = models.ForeignKey(
        CourseAsigned,
        on_delete=models.CASCADE
    )

    weekday = models.IntegerField(
        verbose_name='Día de la semana',
        default=datetime.today().weekday
    )

    starttime = models.TimeField(
        verbose_name='Hora inicio'
    )

    endtime = models.TimeField(
        verbose_name='Hora inicio'
    )

    class Meta:
        verbose_name = 'Horario Curso'
        verbose_name_plural = 'Horarios Cursos'

    def __str__(self):
        return '{0} - {1} : {2} ( {3} - {4} )'.format(
            self.course_asigned.course.name,
            self.course_asigned.level.name,
            self.weekday,
            self.starttime,
            self.endtime
        )

class CourseSession(models.Model):

    course_asigned = models.ForeignKey(
        CourseAsigned,
        on_delete=models.CASCADE
    )

    date = models.ForeignKey(
        Calendar, 
        verbose_name='Fecha',
        on_delete=models.CASCADE
    )

    starttime = models.TimeField(
        verbose_name='Hora inicio'
    )

    endtime = models.TimeField(
        verbose_name='Hora inicio'
    )

    class Meta:
        verbose_name = 'Sesión'
        verbose_name_plural = 'Sesiones'
    
    def __str__(self):
        return '{0} - {1}: {2} ( {3} - {4} )'.format(
            self.course_asigned.course.name,
            self.course_asigned.level.name,
            self.date,
            self.starttime,
            self.endtime
        )