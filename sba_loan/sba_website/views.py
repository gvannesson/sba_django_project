from django.shortcuts import render, redirect
from .models import User, News
from .forms import CreateNews, NewsChangeForm
from django.views.generic import TemplateView, ListView, View
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import User
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomCreationForm, AccountChangeForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin



class HomeView(TemplateView):
    template_name = 'sba_website/home.html'

# Create your views here.

#region Display

class DisplayProfileView(LoginRequiredMixin, TemplateView):
    template_name='sba_website/profile.html'
    login_url= "/login/"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['predictions'] = self.request.user.prediction_set.all().filter(user_id=self.request.user.id) #on rajoute une clé predictions pour savoir s'il y a déjà des prédictions pour ensuite faire apparaître
    #     return context

# region user

class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = User
    template_name= 'sba_website/delete_user_confirm.html'
    success_message='Your account has been deleted successfully!'
    success_url = reverse_lazy('home')


class ClientView(ListView):
    model = User
    template_name = 'sba_website/clients_list.html'
    context_object_name = 'clients'
    def get_queryset(self):
        return User.objects.filter(role = 0)
    
    def dispatch(self, request, *args, **kwargs):

        if not request.user.role: 
            return redirect('/profile/') #renvoie sur cet url si l'utilisateur ne remplit pas la condition is_staff
        return super().dispatch(request, *args, **kwargs)
    
class CreateUserViews(CreateView):
    model = User #spécifie le modèle
    form_class = CustomCreationForm
    template_name = 'sba_website/signup.html' #spécifie le template
    success_url = reverse_lazy('login') #redirection après la création

class AccountUpdateView(UpdateView, LoginRequiredMixin):
    model = User  # Le modèle que l'on souhaite mettre à jour
    form_class=AccountChangeForm
    template_name = 'sba_website/account_update.html'  # Le template à utiliser pour le formulaire
    success_url = reverse_lazy('display_profile')  # L'URL vers laquelle rediriger après la mise à jour réussie

#region News
    
class NewsView(ListView):
    model = News
    template_name = 'sba_website/news_list.html'
    context_object_name = 'news'

    def form_valid(self, form):
        # Associe l'utilisateur connecté à l'article de news avant de sauvegarder
        form.instance.user = self.request.user  # L'utilisateur connecté
        return super().form_valid(form)


# class DeleteUserView(SuccessMessageMixin, DeleteView):
#     model = News
#     template_name= 'sba_website/delete_user_confirm.html'
#     success_message='Your news has been deleted successfully!'
#     success_url = reverse_lazy('home')


class CreateNewsView(CreateView):
    model = News  # Associe le modèle News à cette vue
    form_class = CreateNews  # Le formulaire que tu utilises
    template_name = 'sba_website/create_news.html'  # Template utilisé pour afficher le formulaire
    success_url = reverse_lazy('news_list')  # URL vers laquelle rediriger après la création réussie

    def dispatch(self, request, *args, **kwargs):

        if not request.user.role: 
            return redirect('/profile/') #renvoie sur cet url si l'utilisateur ne remplit pas la condition is_staff
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        form = CreateNews(request.POST)
        
        if form.is_valid():
            news_instance = form.save(commit=False)  
            news_instance.user_id = request.user  
            news_instance.save() 
            return redirect(self.success_url)
        


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'sba_website/delete_news.html'
    context_object_name = 'new'
    success_url = reverse_lazy('news_list')


    def dispatch(self, request, *args, **kwargs):

        if not request.user.role: 
            return redirect('/profile/') #renvoie sur cet url si l'utilisateur ne remplit pas la condition is_staff
        return super().dispatch(request, *args, **kwargs)



class NewsUpdateView(UpdateView, LoginRequiredMixin):
    model = User  # Le modèle que l'on souhaite mettre à jour
    form_class=NewsChangeForm
    template_name = 'sba_website/news_update.html'  # Le template à utiliser pour le formulaire
    success_url = reverse_lazy('new_list')  # L'URL vers laquelle rediriger après la mise à jour réussie

    
    def dispatch(self, request, *args, **kwargs):

        if not request.user.role: 
            return redirect('/profile/') #renvoie sur cet url si l'utilisateur ne remplit pas la condition is_staff
        return super().dispatch(request, *args, **kwargs)


