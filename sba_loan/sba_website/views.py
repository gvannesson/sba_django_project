from django.shortcuts import render
from .models import User, News
# from .forms
from django.views.generic import TemplateView, ListView

class HomeView(TemplateView):
    template_name = 'sba_website/home.html'

# Create your views here.


class ClientView(ListView):
    model = User
    template_name = 'sba_website/clients_list.html'
    context_object_name = 'clients'
    def get_queryset(self):
        return User.objects.filter(role = 0)
    
class NewsView(ListView):
    model = News
    template_name = 'sba_website/news_list.html'
    context_object_name = 'news'
    def get_queryset(self):
        return News.objects.all()
    
# class Crea