from django.shortcuts import render
from .models import User
from django.views.generic import TemplateView, ListView

class HomeView(TemplateView):
    template_name = 'sba_website/home.html'

# Create your views here.


class ClientView(ListView):
    model = User
    template_name = 'sba_website/client_list'
    context_object_name = 'clients'
    def get_queryset(self):
        return self.res