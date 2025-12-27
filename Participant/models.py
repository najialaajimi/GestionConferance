from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.forms import ValidationError

# Create your models here.
def email_validator(value):
    if not value.endswith('esprit.tn'):
        raise ValidationError('Email must end with esprit.tn')
class Participant(AbstractUser):
    cin=models.AutoField(primary_key=True,validators=[RegexValidator(regex='^[0-9]{8}$', message='CIN must be exactly 8 digits.')])
    participant_category=models.CharField(max_length=100,choices=[('étudiant','étudiant'),('enseignant','enseignant'),('doctorant','doctorant'),('chercheur','chercheur')])
    email = models.EmailField(unique=True, validators=[email_validator])
    USERNAME_FIELD = 'username'
    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"