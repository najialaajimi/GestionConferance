from django.contrib import admin
from .models import Participant     
# Register your models here.
@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'participant_category')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('participant_category',)
    ordering = ('username',)