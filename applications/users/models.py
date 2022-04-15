from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

from simple_history.models import HistoricalRecords

class UserManager(BaseUserManager):
    """ Manager Usuarios DotSport """

    def create_user(self, email, doc_num, first_name, last_name, password=None):
        """ Creacion nuevo usuario """
        if not email:
            raise ValueError('Usuario debe tener Email')

        print('*********************')
        print(email)
        
        email = self.normalize_email(email)
        user = self.model(email=email, doc_num=doc_num, first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, doc_num, first_name, last_name, password):
        """ Creacion super usuario """
        user = self.create_user(email, doc_num, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ Modelo Usuario DotSports """

    email = models.EmailField(
        max_length=255, 
        unique=True
    )
    
    doc_num = models.CharField(
        verbose_name='N° Documento',
        max_length=10,
        unique=True,
        null=True
    )

    first_name = models.CharField(
        max_length=255
    )

    last_name = models.CharField(
        max_length=255
    )
    
    is_active = models.BooleanField(
        default=True
    )

    is_staff = models.BooleanField(
        default=False
    )

    avatar = models.ImageField(
        verbose_name='Avatar',
        blank=True,
        upload_to='users',
        null=True
    )

    historical = HistoricalRecords()

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['doc_num','first_name','last_name']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def get_full_name(self):
        """ Obtener nombre completo """
        return '{0} {1}'.format( self.first_name, self.last_name )
    
    def get_short_name(self):
        """ Obtener nombre corto """
        return self.first_name
    
    def __str__(self):
        """ Retorna cadena representativa de usuario """
        return '{0} {1} - {2}'.format( self.first_name, self.last_name, self.email )