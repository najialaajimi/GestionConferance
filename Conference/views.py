from django.shortcuts import render

from Conference.models import Conference, Reservation
from Categorie.models import Category
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.forms import ModelForm, DateInput

# Create your views here.
def ListConferences(request):
    conferences = Conference.objects.all().order_by('start_date')
    categories = Category.objects.all()
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        conferences = conferences.filter(category_id=category_id)
    
    context = {
        'conferences': conferences,
        'categories': categories,
        'selected_category': category_id
    }
    return render(request, 'conference_list.html', context)

class ConferenceDetailView(DetailView):
    model = Conference
    template_name = 'conference_detail.html'
    context_object_name = 'conference'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add reservations for this conference
        context['reservations'] = Reservation.objects.filter(conference=self.object)
        return context

class ConferenceForm(ModelForm):
    class Meta:
        model = Conference
        fields = ['title', 'start_date', 'end_date', 'location', 'price', 'capacity', 'program', 'category']
        widgets = {
            'start_date': DateInput(attrs={'type': 'date'}),
            'end_date': DateInput(attrs={'type': 'date'}),
        }

class ConferenceCreateView(CreateView):
    model = Conference
    form_class = ConferenceForm
    template_name = 'conference_form.html'
    success_url = '/conferences/'

class ConferenceUpdateView(UpdateView):
    model = Conference
    form_class = ConferenceForm
    template_name = 'conference_form.html'
    success_url = '/conferences/'

class ConferenceDeleteView(DeleteView):
    model = Conference
    template_name = 'conference_confirm_delete.html'
    success_url = '/conferences/'