from django.db import models

from applications.locations.models import Location

class Service(models.Model):

    name = models.CharField(
        verbose_name='Nombre',
        max_length=30
    )

    class Meta:
        verbose_name='Servicio'
        verbose_name_plural='Servicios'

    def __str__(self):
        return self.name


class Service_Subcategory(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        verbose_name='Servicio'
    )

    level = models.IntegerField(
        verbose_name='nivel'
    )

    name = models.CharField(
        verbose_name='Nombre',
        max_length=30
    )

    class Meta:
        verbose_name='Subcategoría Servicio'
        verbose_name_plural='Subcategorías Servicio'

    def __str__(self):
        return self.name


class Course(models.Model):

    name = models.CharField(
        verbose_name='Nombre',
        max_length=30
    )

    class Meta:
        verbose_name='Curso'
        verbose_name_plural='Cursos'
    
    def __str__(self):
        return self.name

class Course_Level(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Curso'
    )

    name = models.CharField(
        verbose_name='nivel',
        max_length=30
    )

    level = models.IntegerField(
        verbose_name='nivel'
    )

    class Meta:
        verbose_name='Nivel'
        verbose_name_plural='Niveles'
    
    def __str__(self):
        return '{0} - {1}'.format(
            self.course,
            self.name
        )

class Catalog(models.Model):
    
    location = models.OneToOneField(
        Location,
        on_delete=models.CASCADE,
        verbose_name='Sede'
    )

    services = models.ManyToManyField(
        Service,
        related_name='services',
        verbose_name='Servicios'
    )

    courses = models.ManyToManyField(
        Course,
        related_name='courses',
        verbose_name='Cursos'
    )

    class Meta:
        verbose_name='Catálogo'
        verbose_name_plural='Catálogos'

    def __str__(self):
        return self.location.name