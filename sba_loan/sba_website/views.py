from django.shortcuts import render
from .models import User
from django.views.generic import TemplateView, ListView

class HomeView(TemplateView):
    template_name = 'sba_website/home.html'

# Create your views here.
