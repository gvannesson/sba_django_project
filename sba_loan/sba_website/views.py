from django.shortcuts import render, redirect
from .models import User, News
from .forms import CreateNews
from django.views.generic import TemplateView, ListView, View
from django.urls import reverse_lazy

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


class CreateNewsvView(View):
    template_name = 'sba_website/create_news.html'
    success_url = reverse_lazy('home')
    def get(self,request):
        form = CreateNews()
        return render(request, self.template_name, {'form':form})
    
    
    def post(self, request):

        form = CreateNews(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
