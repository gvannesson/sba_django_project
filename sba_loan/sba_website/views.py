from django.shortcuts import render, redirect
from .models import User, News
from .forms import CreateNews, NewsChangeForm
from django.views.generic import TemplateView, ListView, View
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import User, LoanRequest
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomCreationForm, AccountChangeForm, LoanRequestAdvisorForm, LoanRequestForm, SelectLoanRequest
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import redirect
import api_handler
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse



class HomeView(TemplateView):
    """
    Vue représentant la page d'accueil du site. Cette vue affiche les 5 dernières actualités publiées.

    Attributs :
        template_name (str) : Le nom du template à rendre, ici 'sba_website/home.html'.

    Méthodes :
        get_context_data(**kwargs) : Méthode qui permet d'ajouter des données supplémentaires au contexte du template.
                                      Elle récupère les 5 dernières actualités triées par date de publication (les plus récentes en premier).
    """
    template_name = 'sba_website/home.html'

    def get_context_data(self, **kwargs):
        """
        Récupère les 5 dernières actualités et les ajoute au contexte.

        Args :
            **kwargs : Arguments supplémentaires passés à la méthode (non utilisés ici).

        Retourne :
            dict : Un dictionnaire avec les données à passer au template, y compris les actualités les plus récentes.
        """
        context = super().get_context_data(**kwargs)
        context['news'] = News.objects.all().order_by('-publication_date')[:5]  # Afficher les 5 dernières news
        return context

# Create your views here.

#region Display

class DisplayProfileView(LoginRequiredMixin, TemplateView):
    """
    Vue permettant d'afficher le profil de l'utilisateur connecté.

    Attributs :
        template_name (str) : Le nom du template à rendre, ici 'sba_website/profile.html'.
        login_url (str) : L'URL de la page de connexion à rediriger l'utilisateur si il n'est pas connecté, ici '/login/'.

    Hérite de :
        LoginRequiredMixin : Assure que l'utilisateur est connecté avant d'accéder à cette vue.
        TemplateView : Vue générique de Django permettant de rendre un template avec un contexte.
    """
    template_name='sba_website/profile.html'
    login_url= "/login/"


# region user

class DeleteUserView(SuccessMessageMixin, DeleteView):
    """
    Vue permettant de supprimer un utilisateur du système après confirmation.

    Attributs :
        model (Model) : Le modèle associé à cette vue, ici le modèle `User`.
        template_name (str) : Le nom du template à rendre pour confirmer la suppression, ici 'sba_website/delete_user_confirm.html'.
        success_message (str) : Le message de succès affiché après la suppression du compte, ici 'Your account has been deleted successfully!'.
        success_url (str) : L'URL vers laquelle l'utilisateur est redirigé après la suppression, ici la page d'accueil (définie par `reverse_lazy('home')`).

    Hérite de :
        SuccessMessageMixin : Permet d'afficher un message de succès après l'exécution de l'action.
        DeleteView : Vue générique de Django permettant de supprimer un objet.
    """
    model = User
    template_name= 'sba_website/delete_user_confirm.html'
    success_message='Your account has been deleted successfully!'
    success_url = reverse_lazy('home')


class ClientView(ListView):
    """
    Vue permettant d'afficher la liste des clients dans l'application.

    Attributs :
        model (Model) : Le modèle associé à cette vue, ici le modèle `User`.
        template_name (str) : Le nom du template à rendre, ici 'sba_website/clients_list.html'.
        context_object_name (str) : Le nom de la variable contextuelle qui contiendra la liste des clients dans le template, ici 'clients'.

    Méthodes :
        get_queryset() : Méthode qui retourne la liste des utilisateurs ayant le rôle de client (role = 0).
        dispatch(request, *args, **kwargs) : Méthode qui vérifie si l'utilisateur connecté a un rôle spécifique. Si ce n'est pas le cas, l'utilisateur est redirigé vers son profil. Sinon, la requête est traitée normalement.
    """

    model = User
    template_name = 'sba_website/clients_list.html'
    context_object_name = 'clients'
    def get_queryset(self):
        return User.objects.filter(role = 0)
    
    def dispatch(self, request, *args, **kwargs):

        if request.user.role == 0: 
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
    success_url = reverse_lazy('home')  # L'URL vers laquelle rediriger après la mise à jour réussie

# region Loan

class CreateLoanRequestView(CreateView):
    model = LoanRequest #spécifie le modèle
    form_class = LoanRequestForm
    template_name = 'sba_website/loan_request.html' #spécifie le template
    success_url = reverse_lazy('home') #redirection après la création

    def post(self, request, *args, **kwargs):

        # user = User.objects.get(id = request.user.id)

        # print(user.__dict__)
        # print()
        newrequest = LoanRequest()
        newrequest.user_id = request.user
        newrequest.bank_loan = request.POST.get("bank_loan")
        newrequest.reason = request.POST.get("reason")
        newrequest.save()
        return redirect('/')
    

class FillLoanRequestView(UpdateView):
    model = LoanRequest #spécifie le modèle
    form_class = LoanRequestAdvisorForm
    template_name = 'sba_website/loan_filling.html' #spécifie le template
    success_url = reverse_lazy('select_loan_request') #redirection après la création

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        loan_request = self.get_object()
        loan_request.status = 2
        loan_request.save()
        return response

    def dispatch(self, request, *args, **kwargs):

        if request.user.role == 0: 
            return redirect('/profile/') #renvoie sur cet url si l'utilisateur ne remplit pas la condition is_staff
        return super().dispatch(request, *args, **kwargs)



class LoanListViews(ListView, FormView):
    model = LoanRequest #spécifie le modèle
    form_class = SelectLoanRequest
    template_name = 'sba_website/loan_list.html' #spécifie le template
    context_object_name='loans' #le nom utilisé dans le template

    def get_queryset(self):
        query_company = self.request.GET.get('search_by_company_name')
        query_amount = self.request.GET.get('search_by_amount')
        query_status = self.request.GET.get('search_by_status')
        result = LoanRequest.objects.all()
        if query_company:
            result =  result.filter(user_id= User.objects.get(company_name=query_company).id)
        if query_amount:
            result = result.filter(bank_loan=query_amount)
        if query_status:
            result = result.filter(status=query_status)
        return result


class APITestView(TemplateView):
    template_name = "sba_website/api_test.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
                    "state": "NJ",
                    "term": 45,
                    "no_emp": 45,
                    "urban_rural": 0,
                    "cat_activities": 0,
                    "bank_loan_float": 600000.0,
                    "sba_loan_float": 499998.0,
                    "franchise_code": 0,
                    "lowdoc": False,
                    "bank": "NEW JERSEY ECONOMIC DEVEL"
                    }
       
        context["prediction"] =  api_handler.make_prediction(data)
        return context


class PredictLoanView(DetailView):
    model = LoanRequest
    template_name = 'predict_loan.html'  # Nom de votre template
    context_object_name = 'loan'  # Nom du contexte utilisé dans le template

    def post(self, request, *args, **kwargs):
        loan = self.get_object()  # Récupère le prêt à partir de l'ID dans l'URL
        user = loan.user_id
        print(user)
        data = {
                "state": user.state,
                "term": loan.term,
                "no_emp": user.no_emp,
                "urban_rural": user.urbanrural,
                "cat_activities": user.NAICS[:2],
                "bank_loan_float": loan.bank_loan,
                "sba_loan_float": loan.sba_loan,
                "franchise_code": user.franchisecode,
                "lowdoc": bool(loan.lowdoc),
                "bank": "NEW JERSEY ECONOMIC DEVEL"
                }
        print(data)
        loan.prediction_result = api_handler.make_prediction(data=data)
        loan.status = 3
        loan.save()
        return redirect('/loan_list/')


# class PredictView(TemplateView):
#     template_name = 'sba_website/prediction.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['prediction'] = LoanRequest.objects.all().filter(status=2) #on rajoute une clé predictions pour savoir s'il y a déjà des prédictions pour ensuite faire apparaître
#         return context
    # success_url = reverse_lazy('display_profile')  # L'URL vers laquelle rediriger après la mise à jour réussie

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

        if request.user.role == 0: 
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

        if request.user.role == 0: 
            return redirect('/profile/') #renvoie sur cet url si l'utilisateur ne remplit pas la condition is_staff
        return super().dispatch(request, *args, **kwargs)



class NewsUpdateView(UpdateView, LoginRequiredMixin):
    model = User  # Le modèle que l'on souhaite mettre à jour
    form_class=NewsChangeForm
    template_name = 'sba_website/news_update.html'  # Le template à utiliser pour le formulaire
    success_url = reverse_lazy('new_list')  # L'URL vers laquelle rediriger après la mise à jour réussie


    def dispatch(self, request, *args, **kwargs):

        if request.user.role == 0: 
            return redirect('/profile/') #renvoie sur cet url si l'utilisateur ne remplit pas la condition is_staff
        return super().dispatch(request, *args, **kwargs)


