from django.shortcuts import render
from .models import User, LoanRequest
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomCreationForm, AccountChangeForm, LoanRequestAdvisorForm, LoanRequestForm, SelectLoanRequest
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
import json
from django.shortcuts import redirect
import api_handler

class HomeView(TemplateView):
    template_name = 'sba_website/home.html'

# Create your views here.

class DisplayProfileView(LoginRequiredMixin, TemplateView):
    template_name='sba_website/profile.html'
    login_url= "/login/"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['predictions'] = self.request.user.prediction_set.all().filter(user_id=self.request.user.id) #on rajoute une clé predictions pour savoir s'il y a déjà des prédictions pour ensuite faire apparaître
    #     return context

class DeleteUserView(SuccessMessageMixin, DeleteView):
    model = User
    template_name= 'sba_website/delete_user_confirm.html'
    success_message='Your account has been deleted successfully!'
    success_url = reverse_lazy('home')


class ClientView(ListView):
    model = User
    template_name = 'sba_website/client_list'
    context_object_name = 'clients'
    def get_queryset(self):
        return User.objects.filter(role=0)


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
    success_url = reverse_lazy('home') #redirection après la création

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        loan_request = self.get_object()
        loan_request.status = 2
        loan_request.save()
        return response


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

    def post(self, request, *args, **kwargs):
        return JsonResponse({
                "state": "FL",
                "term": 120,
                "no_emp": 150,
                "urban_rural": 0,
                "cat_activities": 42,
                "bank_loan_float": 120000,
                "sba_loan_float": 100000,
                "franchise_code": 0,
                "lowdoc": True,
                "bank": "NEW JERSEY ECONOMIC DEVEL"
                })
        return super().post(request, *args, **kwargs)

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

    
# class PredictView(TemplateView):
#     template_name = 'sba_website/prediction.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['prediction'] = LoanRequest.objects.all().filter(status=2) #on rajoute une clé predictions pour savoir s'il y a déjà des prédictions pour ensuite faire apparaître
#         return context