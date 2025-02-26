from django import forms
from sba_website.models import User, LoanRequest
from django.contrib.auth.forms import UserCreationForm
from datetime import date


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

class SelectLoanRequest(forms.Form):
    search_by_company_name = forms.ModelChoiceField(label="Company name", queryset=User.objects.values_list('company_name', flat=True).distinct() , required=False)
    search_by_amount = forms.IntegerField(label="Amount", required=False)
    search_by_status = forms.IntegerField(label="Status", required=False)