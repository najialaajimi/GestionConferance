from django.contrib import admin
from .models import Conference, Reservation
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.db.models import Count

# Register your models here.

class ReservationInline(admin.TabularInline):  # Utilisez TabularInline pour format tableau ou StackedInline pour format empilé
    model = Reservation
    extra = 1
    fields = ('participant', 'confirmed', 'reservation_date')
    readonly_fields = ('reservation_date',)
    can_delete = True

# Filtre personnalisé pour le nombre de participants
class ParticipantCountFilter(admin.SimpleListFilter):
    title = _('Participants')
    parameter_name = 'participants'
    
    def lookups(self, request, model_admin):
        return (
            ('no_participants', _('No participants')),
            ('has_participants', _('There are participants')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'no_participants':
            return queryset.annotate(participant_count=Count('reservation')).filter(participant_count=0)
        if self.value() == 'has_participants':
            return queryset.annotate(participant_count=Count('reservation')).filter(participant_count__gt=0)
        return queryset

# Filtre personnalisé pour la date de conférence
class ConferenceDateFilter(admin.SimpleListFilter):
    title = _('Conference Date')
    parameter_name = 'conference_date'
    
    def lookups(self, request, model_admin):
        return (
            ('past', _('Past Conferences')),
            ('today', _('Today Conferences')),
            ('upcoming', _('Upcoming Conferences')),
        )
    
    def queryset(self, request, queryset):
        today = date.today()
        if self.value() == 'past':
            return queryset.filter(start_date__lt=today)
        if self.value() == 'today':
            return queryset.filter(start_date=today)
        if self.value() == 'upcoming':
            return queryset.filter(start_date__gt=today)
        return queryset

@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location')
    search_fields = ('title',)
    list_per_page = 10
    ordering = ('start_date',)
    fieldsets = (
        (None, {
            'fields': ('title', 'location', 'category', 'program')
        }),
        ('Date Information', {
            'fields': ('start_date', 'end_date')
        }),
        ('Capacity and Price', {
            'fields': ('capacity', 'price')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('title', ParticipantCountFilter, ConferenceDateFilter)
    autocomplete_fields = ('category',)
    inlines = [ReservationInline]

@admin.register(Reservation)
class Reservation(admin.ModelAdmin):
    list_display = ('participant', 'conference', 'confirmed', 'reservation_date')
    actions = ['confirm_reservations', 'cancel_reservations']