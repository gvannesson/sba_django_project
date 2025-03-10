from django.shortcuts import render, redirect
from .models import User, News
from .forms import CreateNews, NewsChangeForm
from django.views.generic import TemplateView, ListView, View
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import User, LoanRequest
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView, FormView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomCreationForm, AccountChangeForm, LoanRequestAdvisorForm, LoanRequestForm, SelectLoanRequest, CompanyInfoChangeForm
from django.contrib.auth.views import PasswordChangeView
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
    """
    Vue de création d'un utilisateur.

    Cette vue permet de créer un nouvel utilisateur à partir du formulaire `CustomCreationForm`.
    Lorsqu'un utilisateur est créé avec succès, il est redirigé vers la page de connexion.

    Attributs:
        model (django.db.models.Model): Le modèle `User` qui représente l'utilisateur.
        form_class (django.forms.Form): Le formulaire `CustomCreationForm` utilisé pour collecter les informations de l'utilisateur.
        template_name (str): Le chemin relatif vers le template HTML utilisé pour afficher la page de création.
        success_url (str): L'URL de redirection après la création réussie de l'utilisateur. Dans ce cas, l'utilisateur est redirigé vers la page de connexion.

    Méthodes:
        get_context_data(**kwargs): Cette méthode est héritée de `CreateView` et permet de personnaliser le contexte du template.
        form_valid(form): Cette méthode est héritée de `CreateView` et gère la logique qui se produit lorsque le formulaire est valide.

    Exemple:
        Pour utiliser cette vue, assurez-vous d'avoir le modèle `User` et le formulaire `CustomCreationForm` correctement configurés. Le template `sba_website/signup.html` sera rendu lors de la demande de création.
    """
    model = User #spécifie le modèle
    form_class = CustomCreationForm
    template_name = 'sba_website/signup.html' #spécifie le template
    success_url = reverse_lazy('login') #redirection après la création

class AccountUpdateView(UpdateView, LoginRequiredMixin):
    """
    Vue de mise à jour du compte utilisateur.

    Cette vue permet à un utilisateur connecté de mettre à jour ses informations personnelles.
    Elle utilise le formulaire `AccountChangeForm` et, après une mise à jour réussie, redirige l'utilisateur vers la page d'accueil.

    Attributs:
        model (django.db.models.Model): Le modèle `User` représentant l'utilisateur dont les informations sont mises à jour.
        form_class (django.forms.Form): Le formulaire `AccountChangeForm` utilisé pour modifier les informations de l'utilisateur.
        template_name (str): Le chemin relatif vers le template HTML utilisé pour afficher le formulaire de mise à jour du compte.
        success_url (str): L'URL de redirection après la mise à jour réussie de l'utilisateur. Dans ce cas, l'utilisateur est redirigé vers la page d'accueil.

    Méthodes:
        get_context_data(**kwargs): Cette méthode est héritée de `UpdateView` et permet de personnaliser le contexte du template.
        form_valid(form): Cette méthode est héritée de `UpdateView` et gère la logique qui se produit lorsque le formulaire est valide.
    
    Notes:
        - Seuls les utilisateurs authentifiés peuvent accéder à cette vue, grâce au mixin `LoginRequiredMixin`.
        - Il est nécessaire d'avoir une instance de `User` à mettre à jour dans la vue.

    Exemple:
        Après qu'un utilisateur connecté ait modifié ses informations, la vue redirige automatiquement vers la page d'accueil.
    """
    model = User  # Le modèle que l'on souhaite mettre à jour
    form_class=AccountChangeForm
    template_name = 'sba_website/account_update.html'  # Le template à utiliser pour le formulaire
    success_url = reverse_lazy('home')  # L'URL vers laquelle rediriger après la mise à jour réussie

# region Loan

class CreateLoanRequestView(CreateView):
    """
    Vue de création de demande de prêt.

    Cette vue permet à un utilisateur de soumettre une demande de prêt. Elle utilise le formulaire `LoanRequestForm` pour collecter les informations nécessaires à la création d'une nouvelle demande de prêt. Après avoir soumis une demande, l'utilisateur est redirigé vers la page d'accueil.

    Attributs:
        model (django.db.models.Model): Le modèle `LoanRequest` représentant une demande de prêt.
        form_class (django.forms.Form): Le formulaire `LoanRequestForm` utilisé pour collecter les informations de la demande.
        template_name (str): Le chemin relatif vers le template HTML utilisé pour afficher le formulaire de demande de prêt.
        success_url (str): L'URL de redirection après la création réussie de la demande de prêt. L'utilisateur est redirigé vers la page d'accueil après la soumission.

    Méthodes:
        post(request, *args, **kwargs): Cette méthode est appelée lorsqu'une demande de prêt est soumise via une requête POST. Elle crée un nouvel objet `LoanRequest` et l'associe à l'utilisateur actuellement connecté. Les informations de la demande (montant du prêt et raison) sont récupérées à partir de la requête POST et sauvegardées dans la base de données.

    Notes:
        - L'utilisateur doit être authentifié pour pouvoir soumettre une demande de prêt.
        - Les informations soumises dans le formulaire sont utilisées pour créer une nouvelle instance de `LoanRequest`, qui est ensuite enregistrée en base de données.
        - Cette vue redirige l'utilisateur vers la page d'accueil après la création de la demande.

    Exemple:
        Lorsqu'un utilisateur soumet une demande de prêt, la vue crée une nouvelle demande de prêt associée à l'utilisateur, et l'utilisateur est redirigé vers la page d'accueil.
    """
    model = LoanRequest #spécifie le modèle
    form_class = LoanRequestForm
    template_name = 'sba_website/loan_request.html' #spécifie le template
    success_url = reverse_lazy('home') #redirection après la création

    def post(self, request, *args, **kwargs):
        newrequest = LoanRequest()
        newrequest.user_id = request.user
        newrequest.bank_loan = request.POST.get("bank_loan")
        newrequest.reason = request.POST.get("reason")
        newrequest.save()
        return redirect('/')
    

class FillLoanRequestView(UpdateView):
    """
    Vue de remplissage d'une demande de prêt.

    Cette vue permet à un utilisateur de remplir les détails d'une demande de prêt. Elle utilise le formulaire `LoanRequestAdvisorForm` pour collecter les informations supplémentaires liées à la demande de prêt. Après la soumission du formulaire, le statut de la demande de prêt est mis à jour, et l'utilisateur est redirigé vers une page spécifique.

    Attributs:
        model (django.db.models.Model): Le modèle `LoanRequest` représentant une demande de prêt à mettre à jour.
        form_class (django.forms.Form): Le formulaire `LoanRequestAdvisorForm` utilisé pour collecter des informations supplémentaires pour la demande de prêt.
        template_name (str): Le chemin relatif vers le template HTML utilisé pour afficher le formulaire de remplissage de la demande de prêt.
        success_url (str): L'URL de redirection après la soumission réussie du formulaire. L'utilisateur est redirigé vers la vue `select_loan_request`.

    Méthodes:
        post(request, *args, **kwargs): Cette méthode est appelée lorsqu'une demande de prêt est soumise via une requête POST. Après la soumission, le statut de la demande est mis à jour (le statut passe à `2`), et l'objet `LoanRequest` est sauvegardé en base de données.
        dispatch(request, *args, **kwargs): Cette méthode est utilisée pour vérifier si l'utilisateur a un rôle valide pour accéder à la vue. Si l'utilisateur n'a pas le rôle approprié (si son rôle est `0`), il est redirigé vers la page de son profil.

    Notes:
        - Cette vue est utilisée par les utilisateurs ayant un rôle spécifique pour remplir ou compléter une demande de prêt.
        - Le statut de la demande de prêt est mis à jour après la soumission du formulaire.
        - Si un utilisateur n'a pas les droits appropriés (rôle `0`), il sera redirigé vers sa page de profil.

    Exemple:
        Après avoir rempli et soumis le formulaire, l'utilisateur est redirigé vers la vue `select_loan_request`, et la demande de prêt aura son statut mis à jour à `2`.
    """
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
    """
    Vue de liste des demandes de prêt avec filtres.

    Cette vue affiche une liste de toutes les demandes de prêt, avec la possibilité de filtrer les résultats selon plusieurs critères, tels que le nom de l'entreprise, le montant du prêt, et le statut de la demande. Elle utilise le formulaire `SelectLoanRequest` pour la recherche et affiche les résultats dans le template spécifié.

    Attributs:
        model (django.db.models.Model): Le modèle `LoanRequest` représentant une demande de prêt.
        form_class (django.forms.Form): Le formulaire `SelectLoanRequest` utilisé pour effectuer des recherches et filtrer les demandes de prêt.
        template_name (str): Le chemin relatif vers le template HTML utilisé pour afficher la liste des demandes de prêt.
        context_object_name (str): Le nom de la variable dans le contexte du template qui contiendra la liste des demandes de prêt filtrées. Par défaut, il est défini à `loans`.

    Méthodes:
        get_queryset(): Cette méthode personnalise la requête pour récupérer les demandes de prêt. Elle applique les filtres en fonction des paramètres de recherche présents dans la requête GET (`search_by_company_name`, `search_by_amount`, `search_by_status`). Si des critères de recherche sont fournis, la méthode filtre les demandes de prêt en conséquence.

    Notes:
        - Les filtres suivants sont disponibles pour la recherche:
            - `search_by_company_name`: Filtrer les demandes de prêt par le nom de l'entreprise associée à l'utilisateur.
            - `search_by_amount`: Filtrer les demandes de prêt par le montant du prêt.
            - `search_by_status`: Filtrer les demandes de prêt par leur statut.
        - Si aucun filtre n'est spécifié, toutes les demandes de prêt seront affichées.

    Exemple:
        Lorsqu'un utilisateur souhaite rechercher des demandes de prêt en fonction du nom de l'entreprise, du montant du prêt ou du statut de la demande, il peut utiliser les champs de filtrage. La vue renverra une liste des demandes correspondant aux critères spécifiés.
    """
    model = LoanRequest #spécifie le modèle
    form_class = SelectLoanRequest
    template_name = 'sba_website/loan_list.html' #spécifie le template
    context_object_name='loans' #le nom utilisé dans le template

    def get_queryset(self):
        query_company = self.request.GET.get('search_by_company_name')
        query_amount = self.request.GET.get('search_by_amount')
        query_status = self.request.GET.get('search_by_status')
        result = LoanRequest.objects.all().select_related('user_id')
        if query_company:
            result =  result.filter(user_id= User.objects.get(company_name=query_company).id)
        if query_amount:
            result = result.filter(bank_loan=query_amount)
        if query_status:
            result = result.filter(status=query_status)
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the form instance to the context so your template can render it.
        context['form'] = self.get_form()
        return context


class PredictLoanView(DetailView):
    """
    Vue de prédiction du prêt.

    Cette vue permet de prédire le résultat d'une demande de prêt en utilisant des données spécifiques à l'utilisateur et à la demande. Lorsqu'un utilisateur soumet la demande de prédiction via un formulaire POST, la vue récupère les données nécessaires, effectue la prédiction, met à jour le statut de la demande et redirige l'utilisateur vers la liste des demandes de prêt.

    Attributs:
        model (django.db.models.Model): Le modèle `LoanRequest` représentant une demande de prêt à prédire.
        template_name (str): Le chemin relatif vers le template HTML utilisé pour afficher les détails de la demande de prêt.
        context_object_name (str): Le nom de la variable dans le contexte du template contenant les détails de la demande de prêt. Par défaut, il est défini à `loan`.

    Méthodes:
        post(request, *args, **kwargs): Cette méthode est appelée lorsqu'une requête POST est effectuée. Elle récupère la demande de prêt et l'utilisateur associé, prépare les données nécessaires pour la prédiction, appelle un API de prédiction (via `api_handler.make_prediction`), met à jour le résultat de la prédiction dans la demande de prêt, et change son statut. Ensuite, elle redirige l'utilisateur vers la liste des demandes de prêt.

    Notes:
        - Les données utilisées pour la prédiction incluent des informations de l'utilisateur (comme l'état, le nombre d'employés, le code de franchise, etc.) et des informations de la demande de prêt (comme le montant du prêt, la durée, et le type de prêt).
        - Le statut de la demande de prêt est mis à jour à `3` une fois la prédiction effectuée.
        - La redirection après le traitement se fait vers la vue des demandes de prêt (`/loan_list/`).

    Exemple:
        Lorsqu'un utilisateur soumet une demande de prédiction pour un prêt, la vue appelle un modèle de prédiction externe (API), met à jour les informations de la demande et change son statut, avant de rediriger l'utilisateur vers la page de la liste des prêts.
    """

    model = LoanRequest
    template_name = 'predict_loan.html'  # Nom de votre template
    context_object_name = 'loan'  # Nom du contexte utilisé dans le template
    def post(self, request, *args, **kwargs):
        loan = self.get_object()  # Récupère le prêt à partir de l'ID dans l'URL
        user = loan.user_id
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
        loan.prediction_result = api_handler.make_prediction(data=data)
        loan.status = 3
        loan.save()
        return redirect('/loan_list/')



#region News
    
class NewsView(ListView):

    """
    Vue de liste des articles de news.

    Cette vue affiche une liste d'articles de news. Elle utilise le modèle `News` pour récupérer et afficher les articles dans un template. Le contexte est nommé `news` dans le template, ce qui permet d'accéder facilement à la liste des articles.

    Attributs:
        model (django.db.models.Model): Le modèle `News` représentant les articles de news à afficher.
        template_name (str): Le chemin relatif vers le template HTML utilisé pour afficher la liste des articles de news.
        context_object_name (str): Le nom de la variable dans le contexte du template qui contiendra la liste des articles de news. Par défaut, il est défini à `news`.

    Méthodes:
        form_valid(form): Cette méthode est appelée lorsque le formulaire est valide. Elle associe l'utilisateur connecté à un article de news avant de sauvegarder l'instance de l'article. L'utilisateur est récupéré via `self.request.user` et est affecté à l'instance de `News` avant de procéder à la validation du formulaire.

    Notes:
        - Cette vue est principalement utilisée pour afficher une liste d'articles de news. Si la logique pour la création ou la mise à jour des articles est incluse dans cette vue, la méthode `form_valid` permet d'associer automatiquement l'utilisateur actuel à chaque nouvel article.

    Exemple:
        Lorsqu'un utilisateur soumet un article de news, l'utilisateur connecté est automatiquement associé à cet article avant qu'il ne soit enregistré dans la base de données.
    """
    model = News
    template_name = 'sba_website/news_list.html'
    context_object_name = 'news'

    def form_valid(self, form):
        # Associe l'utilisateur connecté à l'article de news avant de sauvegarder
        form.instance.user = self.request.user  # L'utilisateur connecté
        return super().form_valid(form)




class CreateNewsView(CreateView):
    """
    Vue de création d'un article de news.

    Cette vue permet à un utilisateur d'ajouter un nouvel article de news en remplissant un formulaire. Si la création est réussie, l'utilisateur est redirigé vers la liste des articles de news. La vue vérifie également que l'utilisateur a un rôle approprié avant d'afficher le formulaire.

    Attributs:
        model (django.db.models.Model): Le modèle `News` qui représente un article de news à créer.
        form_class (django.forms.Form): Le formulaire `CreateNews` utilisé pour collecter les informations nécessaires à la création d'un article de news.
        template_name (str): Le chemin relatif vers le template HTML utilisé pour afficher le formulaire de création d'un article de news.
        success_url (str): L'URL de redirection après la création réussie de l'article de news. L'utilisateur est redirigé vers la liste des articles de news (`news_list`).

    Méthodes:
        dispatch(request, *args, **kwargs): Cette méthode vérifie le rôle de l'utilisateur. Si l'utilisateur n'a pas un rôle approprié (si son rôle est `0`), il est redirigé vers la page de profil. Sinon, elle appelle la méthode `dispatch` de la classe parente pour continuer l'exécution normale.
        post(request): Cette méthode est appelée lorsqu'une requête POST est effectuée pour soumettre le formulaire. Elle crée un nouvel article de news et l'associe à l'utilisateur connecté avant de sauvegarder l'article dans la base de données. Ensuite, elle redirige l'utilisateur vers la liste des articles de news.

    Notes:
        - Cette vue est utilisée pour la création d'un article de news par un utilisateur ayant les droits appropriés.
        - Si l'utilisateur n'a pas les droits nécessaires (rôle `0`), il sera redirigé vers la page de son profil.
        - La méthode `post` permet de personnaliser le processus de sauvegarde en associant l'utilisateur connecté au nouvel article avant de le sauvegarder.

    Exemple:
        Lorsqu'un utilisateur soumet un nouvel article de news via le formulaire, l'article est enregistré avec l'utilisateur connecté comme auteur, et l'utilisateur est redirigé vers la liste des articles de news après la création.
    """

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
    """
    Vue de suppression d'un article de news.

    Cette vue permet à un utilisateur de supprimer un article de news. Avant de procéder à la suppression, la vue vérifie que l'utilisateur a le rôle approprié pour effectuer cette action. Si l'utilisateur n'a pas les droits nécessaires, il est redirigé vers sa page de profil.

    Attributs:
        model (django.db.models.Model): Le modèle `News` représentant l'article de news à supprimer.
        template_name (str): Le chemin relatif vers le template HTML utilisé pour confirmer la suppression de l'article.
        context_object_name (str): Le nom de la variable dans le contexte du template qui contient l'article de news à supprimer. Par défaut, il est défini à `new`.
        success_url (str): L'URL de redirection après la suppression réussie de l'article de news. L'utilisateur est redirigé vers la liste des articles de news (`news_list`).

    Méthodes:
        dispatch(request, *args, **kwargs): Cette méthode vérifie le rôle de l'utilisateur. Si l'utilisateur n'a pas un rôle approprié (si son rôle est `0`), il est redirigé vers la page de profil. Sinon, elle appelle la méthode `dispatch` de la classe parente pour continuer l'exécution normale.

    Notes:
        - Cette vue est utilisée pour la suppression d'un article de news. Avant de permettre la suppression, la vue vérifie que l'utilisateur a un rôle valide pour effectuer l'action.
        - Une fois l'article supprimé, l'utilisateur est redirigé vers la liste des articles de news.

    Exemple:
        Lorsqu'un utilisateur ayant un rôle approprié supprime un article de news, la vue supprime l'article et redirige l'utilisateur vers la page de la liste des articles de news.
    """

    model = News
    template_name = 'sba_website/delete_news.html'
    context_object_name = 'new'
    success_url = reverse_lazy('news_list')


    def dispatch(self, request, *args, **kwargs):

        if request.user.role == 0: 
            return redirect('/profile/') #renvoie sur cet url si l'utilisateur ne remplit pas la condition is_staff
        return super().dispatch(request, *args, **kwargs)



class NewsUpdateView(UpdateView, LoginRequiredMixin):
    """
    Vue de mise à jour d'un article de news.

    Cette vue permet à un utilisateur de modifier un article de news existant. Elle vérifie également que l'utilisateur a les permissions appropriées avant de permettre la mise à jour. Si l'utilisateur n'a pas les droits nécessaires, il est redirigé vers sa page de profil.

    Attributs:
        model (django.db.models.Model): Le modèle `User` utilisé dans cette vue, bien que ce soit probablement une erreur, car il devrait probablement être `News` pour gérer les articles de news.
        form_class (django.forms.Form): Le formulaire `NewsChangeForm` utilisé pour la modification des articles de news.
        template_name (str): Le chemin relatif vers le template HTML utilisé pour afficher le formulaire de mise à jour.
        success_url (str): L'URL de redirection après la mise à jour réussie de l'article de news. L'utilisateur est redirigé vers la liste des articles de news (`news_list`).

    Méthodes:
        dispatch(request, *args, **kwargs): Cette méthode vérifie le rôle de l'utilisateur. Si l'utilisateur n'a pas un rôle approprié (si son rôle est `0`), il est redirigé vers la page de profil. Sinon, elle appelle la méthode `dispatch` de la classe parente pour continuer l'exécution normale.

    Notes:
        - Cette vue permet à un utilisateur de mettre à jour un article de news existant. Le formulaire permet de modifier les champs définis dans le modèle `News`.
        - Si l'utilisateur n'a pas les droits nécessaires (rôle `0`), il sera redirigé vers sa page de profil.
        - L'attribut `model` devrait probablement être `News`, car c'est un article de news qui est mis à jour, et non un utilisateur. Cela semble être une erreur dans la définition de la classe.

    Exemple:
        Lorsqu'un utilisateur ayant un rôle approprié modifie un article de news, la vue permet de mettre à jour les informations de l'article et redirige ensuite l'utilisateur vers la liste des articles de news après la mise à jour.
    """

    model = News  # Le modèle que l'on souhaite mettre à jour
    form_class=NewsChangeForm
    template_name = 'sba_website/news_update.html'  # Le template à utiliser pour le formulaire
    success_url = reverse_lazy('news_list')  # L'URL vers laquelle rediriger après la mise à jour réussie


    def dispatch(self, request, *args, **kwargs):

        if request.user.role == 0: 
            return redirect('/profile/') #renvoie sur cet url si l'utilisateur ne remplit pas la condition is_staff
        return super().dispatch(request, *args, **kwargs)

class CustomPassWordChangeView(PasswordChangeView):
    success_url = reverse_lazy("password_change_done")
    template_name = "sba_website/password_change.html"
    title = ("Password change")

class CompanyUpdateView(UpdateView, LoginRequiredMixin):
    model = User
    form_class=CompanyInfoChangeForm
    template_name = 'sba_website/company_info_update.html'
    
    def form_valid(self, form):
        form.save()
        user = self.request.user
        if user.role == 1:
            return redirect('clients_list')
        else:
            return redirect('display_profile') 
    
    