from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    SEXO_FEMENINO = 'F'
    SEXO_MASCULINO = 'M'
    SEXO_CHOICES = (
        (SEXO_FEMENINO, 'Femenino'),
        (SEXO_MASCULINO, 'Masculino')
    )
    sex = models.CharField('Sexo', max_length=1, choices=SEXO_CHOICES)
    username = models.CharField('Username', max_length=50, unique=True)
