from django.shortcuts import render
from .models import User
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(TemplateView):
    template_name = 'sba_website/home.html'

# Create your views here.

class DisplayProfileView(LoginRequiredMixin, TemplateView):
    template_name='sba_website/profile.html'
    login_url= "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['predictions'] = self.request.user.prediction_set.all().filter(user_id=self.request.user.id) #on rajoute une clé predictions pour savoir s'il y a déjà des prédictions pour ensuite faire apparaître
        return context

class ClientView(ListView):
    model = User
    template_name = 'sba_website/client_list'
    context_object_name = 'clients'
    def get_queryset(self):
        return self.res
