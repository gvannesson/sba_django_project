from django.urls import path
from .views import HomeView,ClientView, NewsView,CreateNewsView,NewsDeleteView,NewsUpdateView
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView, DisplayProfileView, CreateUserViews
from .views import DeleteUserView, AccountUpdateView, CreateLoanRequestView, FillLoanRequestView, LoanListViews, PredictLoanView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('clients_list/', ClientView.as_view(), name='clients_list'),
    path('news_list/', NewsView.as_view(), name='news_list'),
    path('create_news/', CreateNewsView.as_view(), name='create_news'),
    path('signup/', CreateUserViews.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='sba_website/login.html'), name='login'),
    path ("logout/", LogoutView.as_view(), name="logout"),
    path("delete_user/<int:pk>/", DeleteUserView.as_view(), name='delete_user'), 
    path ("<int:pk>/acc_update/", AccountUpdateView.as_view(), name="account_update"),
    path ("<int:pk>/news_update/", NewsUpdateView.as_view(), name="news_update"),
    path('profile/', DisplayProfileView.as_view(), name='display_profile'),
    path('loan_list/', LoanListViews.as_view(), name='select_loan_request'),
    path('loan_request/', CreateLoanRequestView.as_view(), name='create_loan_request'),
    path('loan_filling/<int:pk>/', FillLoanRequestView.as_view(), name='fill_loan_request'),
    path('delete_news/<int:pk>/', NewsDeleteView.as_view(), name='delete_news'),
    path('predict_loan/<int:pk>/', PredictLoanView.as_view(), name='predict_loan')
]