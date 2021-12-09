import datetime

from django.db import models
from applications.users.models import User

class Location(models.Model):
    """ Sucursal Gimnasio """
    
    id = models.BigAutoField(
        primary_key=True,
        verbose_name= 'Id Sede'
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name= 'Nombre Sede',
        unique=True,
        null=False
    )
    
    address = models.CharField(
        verbose_name= 'Direccion',
        max_length=255,
        null=False
    )

    city = models.CharField(
        verbose_name='Ciudad',
        max_length=50,
        null=False
    )

    id_region = models.CharField(
        verbose_name='Id Region',
        max_length=5
    )

    region = models.CharField(
        verbose_name='Nombre Region',
        max_length=50,
        null=False
    )

    phone = models.CharField(
        verbose_name='Teléfono',
        max_length=15,
        null=True
    )

    # manager = models.ManyToManyField(
    #     'employees.Employee',
    #     related_name='manager_location'
    # )

    created_at = models.DateTimeField(
        null=False,
        default=datetime.datetime.today()
    )

    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='location_created_by'
    )

    updated_at = models.DateTimeField(
        blank=True
    )

    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'Sede'
        verbose_name_plural = 'Sedes'

    def __str__(self):
        return self.name

    def get_address(self):
        return '{0}, {1}, {2}'.format(self.address, self.city, self.region)



class Pool(models.Model):
    """ Piscina Deportiva """

    id = models.BigAutoField(
        primary_key=True,
        verbose_name='Id Piscina'
    )

    name = models.CharField(
        verbose_name='Nombre',
        max_length=50,
        null=False,
        unique=True
    )

    id_location = models.ForeignKey(
        Location,
        verbose_name='Sedes',
        related_name='pools',
        on_delete=models.CASCADE
    )

    lanes = models.IntegerField(
        verbose_name='Cantidad Carriles',
        null=False,
        default=10
    )

    width = models.DecimalField(
        verbose_name='Ancho (mt)',
        max_digits=5,
        decimal_places=2,
        null=False
    )

    length = models.DecimalField(
        verbose_name='Largo (mt)',
        max_digits=5,
        decimal_places=2,
        null=False
    )

    min_depth = models.DecimalField(
        verbose_name='Profundidad mínima (mt)',
        max_digits=5,
        decimal_places=2,
        null=False
    )

    max_depth = models.DecimalField(
        verbose_name='Profundidad máxima (mt)',
        max_digits=5,
        decimal_places=2,
        null=False
    )

    is_available = models.BooleanField(
        verbose_name='Disponible',
        default=False
    )

    created_at = models.DateTimeField(
        null=False,
        default=datetime.datetime.today()
    )

    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='lane_created_by'
    )

    updated_at = models.DateTimeField(
        null=True
    )

    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='lane_updated_by'
    )

    class Meta:
        verbose_name = 'Piscina'
        verbose_name_plural = 'Piscinas'

    def __str__(self):

        return '{0} - {1}'.format( self.id_location.name, self.name )
    

class Lane(models.Model):

    id = models.BigAutoField(
        primary_key=True,
        verbose_name='Id Carril'
    )

    id_pool = models.ForeignKey(
        Pool,
        on_delete=models.CASCADE,
        verbose_name='Piscina'
    )

    lane_no = models.IntegerField(
        verbose_name='N° Carril'
    )

    class Meta:
        verbose_name = 'Carril'
        verbose_name_plural = 'Carriles'
    
    def __str__(self):
        return '{0}, Carril N° {1}'.format( self.id_pool, self.lane_no )