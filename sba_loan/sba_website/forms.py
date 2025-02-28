from django import forms 
from .models import News
from django import forms
from sba_website.models import User, LoanRequest
from django.contrib.auth.forms import UserCreationForm
from datetime import date



class CreateNews(forms.ModelForm):
    """
    Formulaire permettant de créer une nouvelle actualité.

    Attributs :
        model (Model) : Le modèle associé à ce formulaire, ici le modèle `News`.
        fields (list) : Liste des champs du modèle à inclure dans le formulaire.
        widgets (dict) : Définition des widgets personnalisés pour certains champs, ici le champ `date_news`
                         qui utilise un champ de saisie de date avec un format spécifique.
    """

    class Meta:
        model = News
        fields = ['topic','date_news','content','news_url', 'publication_date']
        widgets = {'date_news': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'})}

class NewsChangeForm(forms.ModelForm):
    """
    Formulaire permettant de modifier les informations d'une actualité existante.

    Attributs :
        model (Model) : Le modèle associé à ce formulaire, ici le modèle `News`.
        fields (list) : Liste des champs du modèle `News` à inclure dans le formulaire pour la modification. 
                        Ici, il s'agit de `date_news`, `news_url`, `content` et `topic`.
    """
    class Meta:
        model = News
        fields = ['date_news','news_url','content','topic'] 


class CustomCreationForm(UserCreationForm):
    """
    Formulaire personnalisé pour la création d'un utilisateur avec des informations supplémentaires.

    Attributs :
        model (Model) : Le modèle associé à ce formulaire, ici le modèle `User`.
        fields (list) : Liste des champs du modèle `User` à inclure dans le formulaire pour la création.
                        Ici, il s'agit de `email`, `company_name`, `password1`, `password2`, `NAICS`, 
                        `franchisecode`, `state`, `no_emp`, `urbanrural`, et `phone_number`.
    """

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["email", 'company_name', "password1", "password2", 'NAICS', 'franchisecode', 'state','no_emp', 'urbanrural','phone_number'] #les champs utilisés pour la création d'un profil

class AccountChangeForm(forms.ModelForm):
    """
    Formulaire permettant de modifier les informations d'un utilisateur, telles que l'email et le numéro de téléphone.

    Attributs :
        model (Model) : Le modèle associé à ce formulaire, ici le modèle `User`.
        fields (list) : Liste des champs du modèle `User` à inclure dans le formulaire pour la modification.
                        Ici, il s'agit de `email` et `phone_number`.
    """

    class Meta:
        model = User
        fields = ['email','phone_number'] #les champs mis à jour lors de l'update du profil

class LoanRequestForm(forms.ModelForm):
    """
    Formulaire permettant de soumettre une demande de prêt avec le montant du prêt bancaire et la raison de la demande.

    Attributs :
        model (Model) : Le modèle associé à ce formulaire, ici le modèle `LoanRequest`.
        fields (list) : Liste des champs du modèle `LoanRequest` à inclure dans le formulaire. 
                        Ici, il s'agit de `bank_loan` et `reason`.
    """

    class Meta:
        model = LoanRequest
        fields = ['bank_loan', 'reason'] #les champs mis à jour lors de l'update du profil


class LoanRequestAdvisorForm(forms.ModelForm):
    """
    Formulaire permettant à un conseiller de soumettre des informations supplémentaires pour une demande de prêt.

    Attributs :
        model (Model) : Le modèle associé à ce formulaire, ici le modèle `LoanRequest`.
        fields (list) : Liste des champs du modèle `LoanRequest` à inclure dans le formulaire pour l'avis du conseiller.
                        Ici, il s'agit de `lowdoc`, `sba_loan`, `revlinecr`, et `term`.
    """
    class Meta:
        model = LoanRequest
        fields = ['lowdoc', 'sba_loan', 'revlinecr', 'term'] #les champs mis à jour lors de l'update du profil

class SelectLoanRequest(forms.Form):

    """
    Formulaire permettant de filtrer les demandes de prêt en fonction de différents critères.

    Attributs :
        search_by_company_name (ModelChoiceField) : Champ permettant de rechercher les demandes de prêt par le nom de l'entreprise.
                                                   Il permet de sélectionner un nom d'entreprise parmi ceux enregistrés.
        search_by_amount (IntegerField) : Champ permettant de rechercher les demandes de prêt par montant.
        search_by_status (IntegerField) : Champ permettant de rechercher les demandes de prêt par statut (par exemple, en attente, approuvée, rejetée).
    """
    search_by_company_name = forms.ModelChoiceField(label="Company name", queryset=User.objects.values_list('company_name', flat=True).distinct() , required=False)
    search_by_amount = forms.IntegerField(label="Amount", required=False)
    search_by_status = forms.IntegerField(label="Status", required=False)