from django.shortcuts import redirect, render

from Categorie.models import Category
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView
from django.forms import ModelForm

# Create your views here.
def list_categories(request):
    categories = Category.objects.all().order_by('title')
    return render(request, 'category_list.html', {'categories': categories})
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'
class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category_form.html'
    fields = ['title']
    success_url = '/categories/'
class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'category_form.html'
    fields = ['title']
    success_url = '/categories/'
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = '/categories/'

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['title']