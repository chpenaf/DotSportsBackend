from django.db import models

class Application(models.Model):

    id = models.BigAutoField(
        primary_key=True,
        verbose_name='Id'
    )

    name = models.CharField(
        max_length=30,
        verbose_name='Nombre Tecnico',
        null=False
    )

    path = models.CharField(
        max_length=50,
        verbose_name='Ruta',
        null=False
    )

    icon = models.CharField(
        max_length=15,
        verbose_name='Icono'
    )

    text = models.CharField(
        max_length=30,
        verbose_name='Titulo',
        null=False
    )

    position = models.IntegerField(
        verbose_name='Posicion'
    )

    admin = models.BooleanField(
        verbose_name='Administrador',
        null=True,
        blank=True
    )

    staff = models.BooleanField(
        verbose_name='Empleado',
        null=True,
        blank=True
    )

    member = models.BooleanField(
        verbose_name='Miembro',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Aplicación'
        verbose_name_plural = 'Aplicaciones'
    
    def __str__(self):
        return self.text