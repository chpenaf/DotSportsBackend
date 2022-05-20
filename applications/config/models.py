from django.db import models

from applications.locations.models import Location, Pool

class CapacityPool(models.Model):

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        verbose_name='Sede'
    )

    pool = models.ForeignKey(
        Pool,
        on_delete=models.CASCADE,
        verbose_name='Piscina'
    )

    capacity_lane = models.IntegerField(
        verbose_name='Capacidad por carril',
        default=10
    )

    begin_validity = models.DateField(
        verbose_name='Inicio Validez'
    )

    end_validity = models.DateField(
        verbose_name='Fin Validez'
    )

    class Meta:
        verbose_name='Aforo por Piscina'
        verbose_name_plural='Aforo por Piscina'
    
    def __str__(self):
        return '{0}: {1}'.format(
            self.pool.name,
            self.capacity_lane
        )