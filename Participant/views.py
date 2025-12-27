from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import Participant

# Create your views here.
class ParticipantLoginView(LoginView):
    template_name = 'participant_login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('conference_list')

class ParticipantLogoutView(LogoutView):
    next_page = reverse_lazy('participant_login')

class ParticipantRegisterView(CreateView):
    model = Participant
    template_name = 'participant_register.html'
    fields = ['username', 'email', 'first_name', 'last_name', 'participant_category', 'password']
    success_url = reverse_lazy('participant_login')
    
    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)
