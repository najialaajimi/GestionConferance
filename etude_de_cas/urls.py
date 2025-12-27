"""
URL configuration for etude_de_cas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Conference import views as conference_views
from Categorie import views as category_views
from Participant import views as participant_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('conferences/', conference_views.ListConferences, name='conference_list'),    
    path('conferences/<int:pk>/', conference_views.ConferenceDetailView.as_view(), name='conference_detail'),
    path('conferences/create/', conference_views.ConferenceCreateView.as_view(), name='conference_create'),
    path('conferences/<int:pk>/update/', conference_views.ConferenceUpdateView.as_view(), name='conference_update'),
    path('conferences/<int:pk>/delete/', conference_views.ConferenceDeleteView.as_view(), name='conference_delete'),
    path('categories/', category_views.list_categories, name='category_list'),
    path('categories/<int:pk>/', category_views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/create/', category_views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', category_views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', category_views.CategoryDeleteView.as_view(), name='category_delete'),
    path('login/', participant_views.ParticipantLoginView.as_view(), name='participant_login'),
    path('logout/', participant_views.ParticipantLogoutView.as_view(), name='participant_logout'),
    path('register/', participant_views.ParticipantRegisterView.as_view(), name='participant_register'),
    path('', participant_views.ParticipantLoginView.as_view(), name='home'),
]
