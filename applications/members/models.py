import datetime

from dateutil.relativedelta import relativedelta

from django.db import models

from applications.users.models import User

class Member(models.Model):

    PENDING  = 'PE'
    ACTIVE   = 'AC'
    INACTIVE = 'IN'

    MEMBER_STATUS_CHOICES = [
        ( PENDING, 'Pendiente' ),
        ( ACTIVE, 'Activo' ),
        ( INACTIVE, 'Inactivo' ),
    ]

    id = models.BigAutoField(
        primary_key=True,
        verbose_name='Id Miembro'
    )

    doc_num = models.CharField(
        max_length=10,
        verbose_name='N° Documento',
        null=False,
        unique=True
    )

    first_name = models.CharField(
        max_length=50,
        verbose_name='Nombre(s)',
        null=False
    )

    last_name = models.CharField(
        max_length=50,
        verbose_name='Apellido(s)',
        null=False
    )

    date_of_birth = models.DateField(
        verbose_name='Fecha de Nacimiento',
        null=False
    )

    sex = models.CharField(
        max_length=1,
        verbose_name='Sexo',
        null=False
    )

    status = models.CharField(
        max_length=2,
        verbose_name='Status',
        choices=MEMBER_STATUS_CHOICES,
        default=PENDING
    )

    user = models.OneToOneField(
        User,
        null=True,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        null=False,
        default=datetime.datetime.now()
    )

    created_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name='member_created_by'
    )

    updated_at = models.DateTimeField(
        blank=True,
        null=True
    )

    updated_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='member_updated_by'
    )

    canceled_at = models.DateTimeField(
        blank=True,
        null=True
    )

    canceled_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='member_canceled_by'
    )

    class Meta:
        verbose_name = 'Miembro'
        verbose_name_plural = 'Miembros'

    def __str__(self):
        """ retorna Numero de documento + Nombre del miembro """
        return '{0}, {1}'.format(self.last_name, self.first_name)

    def get_short_name(self):
        """ Obtiene nombre completo del miembre """
        return '{0} {1}'.format(self.first_name, self.last_name)

    def get_age(self, today=None) -> str:
        """ Obtiene edad del miembro """
        if today is None:
            today = datetime.date.today()

        return relativedelta( today, self.date_of_birth ).years
