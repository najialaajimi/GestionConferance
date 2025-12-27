from django.db import models
from PIL import Image
from django.core.validators import MaxValueValidator,FileExtensionValidator,MinValueValidator
from django.db.models import Q
from datetime import date
from django.forms import ValidationError
# Create your models here.
class Conference(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField(validators=[MaxValueValidator(500)])
    program = models.FileField(upload_to='programs/', validators=[FileExtensionValidator(allowed_extensions=['pdf','doc','docx'])], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category= models.ForeignKey('Categorie.Category', on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Conference"
        verbose_name_plural = "Conferences"
        constraints = [
            models.CheckConstraint(
                condition=Q(start_date__gt=date.today()),
                name='start_date_must_be_future'
            )
        ]
    def clean(self):
        # Vérifier que la date de début est supérieure à la date système
        if self.start_date and self.start_date <= date.today():
            raise ValidationError('Start date must be greater than today.')
        
        # Vérifier que la date de fin est après la date de début
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError('End date must be after start date.')
    def __str__(self):
        return self.title
class Reservation(models.Model):
    participant = models.ForeignKey('Participant.Participant', on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    reservation_date = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
    
    def clean(self):
        # Vérifier que la conférence est à venir
        if self.conference.start_date < date.today():
            raise ValidationError('Cannot make a reservation for a conference that has already started.')
        
        # Vérifier qu'il n'y a pas déjà une réservation pour cette conférence
        if self.pk is None:  # Nouvelle réservation seulement
            if Reservation.objects.filter(participant=self.participant, conference=self.conference).exists():
                raise ValidationError('You have already made a reservation for this conference.')
        
        # Vérifier la capacité de la conférence
        if Reservation.objects.filter(conference=self.conference, confirmed=True).count() >= self.conference.capacity:
            raise ValidationError('This conference is fully booked.')
        
        # Limiter le nombre de conférences par jour (max 3 par jour)
        conference_date = self.conference.start_date
        reservations_same_day = Reservation.objects.filter(
            participant=self.participant,
            conference__start_date=conference_date
        )
        
        # Exclure la réservation actuelle si on modifie
        if self.pk is not None:
            reservations_same_day = reservations_same_day.exclude(pk=self.pk)
        
        if reservations_same_day.count() >= 3:
            raise ValidationError(f'You cannot reserve more than 3 conferences on the same day ({conference_date}).')