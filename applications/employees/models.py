import datetime

from django.db import models

from applications.locations.models import Location
from applications.users.models import User

class Employee(models.Model):
    """ Empleados """

    RECEPCIONISTA = 'RE'
    ADMINISTRADOR = 'AD'

    JOBS_CHOICES = [
        ( RECEPCIONISTA, 'Recepcionista' ),
        ( ADMINISTRADOR, 'Administrador' ),
    ]

    id = models.BigAutoField(
        verbose_name='Id Empleado',
        primary_key=True
    )

    doc_num = models.CharField(
        verbose_name='N° Documento',
        max_length=10,
        unique=True,
        null=False
    )

    first_name = models.CharField(
        verbose_name='Nombre(s)',
        max_length=50
    )

    last_name = models.CharField(
        verbose_name='Apellido(s)',
        max_length=50
    )

    date_of_birth = models.DateField(
        verbose_name='Fecha de Nacimiento',
        null=True
    )

    sex = models.CharField(
        max_length=1,
        verbose_name='Sexo',
        null=False
    )

    job = models.CharField(
        verbose_name='Trabajo',
        max_length=2,
        choices=JOBS_CHOICES,
        default=RECEPCIONISTA
    )

    hire_date = models.DateField(
        verbose_name='Fecha contratación',
        null=True
    )

    location = models.ForeignKey(
        Location,
        verbose_name='Sede',
        null=True,
        on_delete=models.CASCADE
    )

    user = models.OneToOneField(
        User,
        verbose_name='Usuario',
        null=True,
        on_delete=models.CASCADE
    )

    is_active = models.BooleanField(
        null=True,
        default=True
    )

    created_at = models.DateTimeField(
        null=False,
        default=datetime.datetime.today()
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='employee_created_by'
    )

    updated_at = models.DateTimeField(
        null=True
    )

    updated_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='employee_updated_by'
    )

    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'

    def __str__(self):
        return '{0} - {1}'.format(self.id_employee,self.get_full_name())

    def get_full_name(self):
        return '{0}, {1}'.format( self.last_name, self.first_name )