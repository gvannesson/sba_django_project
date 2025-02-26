from django import forms 
from .models import News
from django import forms
from sba_website.models import User, LoanRequest
from django.contrib.auth.forms import UserCreationForm
from datetime import date



class CreateNews(forms.ModelForm):
    class Meta:
        model = News
        fields = ['topic','date_news','content','news_url', 'publication_date']
        widgets = {'date_news': forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'})}

class NewsChangeForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['date_news','news_url','content','topic'] 


class CustomCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["email", "password1", "password2", 'NAICS', 'state','company_name','urbanrural','phone_number'] #les champs utilisés pour la création d'un profil

class AccountChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email','phone_number'] #les champs mis à jour lors de l'update du profil

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['bank_loan', 'reason'] #les champs mis à jour lors de l'update du profil


class LoanRequestAdvisorForm(forms.ModelForm):
    class Meta:
        model = LoanRequest
        fields = ['lowdoc', 'sba_loan', 'revlinecr', 'term'] #les champs mis à jour lors de l'update du profil

