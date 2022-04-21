from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.db import models

from applications.employees.models import Employee
from applications.locations.models import Location
from applications.members.models import Member


class Credit_Header(models.Model):

    ACTIVE   = 'AC'
    FINISHED = 'FI'
    CANCELED = 'CA'

    HEADER_STATUS_CHOICES = [
        ( ACTIVE, 'Activo' ),
        ( FINISHED, 'Finalizado' ),
        ( CANCELED, 'Cancelado' )
    ]

    location = models.ForeignKey(
        Location,
        on_delete = models.SET_NULL,
        null=True
    )

    member = models.ForeignKey(
        Member,
        on_delete = models.DO_NOTHING
    )

    quantity = models.IntegerField(
        verbose_name = 'Cantidad'
    )

    status = models.CharField(
        verbose_name = 'Status',
        max_length = 2,
        choices = HEADER_STATUS_CHOICES,
        default = ACTIVE 
    )

    begin_validity = models.DateField(
        verbose_name = 'Inicio validez',
        default = datetime.now().date()
    )

    end_validity = models.DateField(
        verbose_name = 'Fin validez',
        default = ( datetime.today() + relativedelta( months = +1 ) ).date()
    )

    entered_by = models.ForeignKey(
        Employee,
        on_delete = models.DO_NOTHING
    )

    doc_ref = models.CharField(
        verbose_name = 'Documento de referencia',
        max_length=30
    )

    class Meta:
        verbose_name = 'Crédito (cabecera)'
        verbose_name_plural = 'Créditos (cabecera)'
    
    def __str__(self):
        return '{0}'.format(self.member)
    
    
class Credit_Pos(models.Model):

    AVAILABLE = 'AV'
    RESERVED  = 'RE'
    COMPLETED = 'CO'

    CREDIT_STATUS_CHOICES = [
        ( AVAILABLE, 'Disponible' ),
        ( RESERVED, 'Reservado' ),
        ( COMPLETED, 'Completado' )
    ]

    header = models.ForeignKey(
        Credit_Header,
        on_delete = models.CASCADE,
        verbose_name ='Cabecera'
    )

    pos = models.IntegerField(
        verbose_name = 'Posición'
    )

    begin_validity = models.DateField(
        verbose_name = 'Inicio validez',
        default = datetime.now().date()
    )

    end_validity = models.DateField(
        verbose_name = 'Fin validez',
        default = ( datetime.today() + relativedelta( months = +1 ) )
    )

    status = models.CharField(
        verbose_name='Status',
        max_length=2,
        choices=CREDIT_STATUS_CHOICES,
        default=AVAILABLE
    )

    used_at = models.DateField(
        verbose_name='Usado el',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Crédito (posición)'
        verbose_name_plural = 'Créditos (posición)'
    
    def __str__(self):
        return 'Credit: {0} - ( {1} / {2} )'.format(
            self.header.id,
            self.pos,
            self.header.quantity
            )
