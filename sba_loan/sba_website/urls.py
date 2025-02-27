from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView, DisplayProfileView, CreateUserViews
from .views import DeleteUserView, AccountUpdateView, CreateLoanRequestView, FillLoanRequestView, LoanListViews, APITestView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', CreateUserViews.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='sba_website/login.html'), name='login'),
    path ("logout/", LogoutView.as_view(), name="logout"),
    path("delete_user/<int:pk>/", DeleteUserView.as_view(), name='delete_user'), 
    path ("<int:pk>/acc_update/", AccountUpdateView.as_view(), name="account_update"),
    path('profile/', DisplayProfileView.as_view(), name='display_profile'),
    path('loan_list/', LoanListViews.as_view(), name='select_loan_request'),
    path('loan_request/', CreateLoanRequestView.as_view(), name='create_loan_request'),
    path('loan_filling/<int:pk>/', FillLoanRequestView.as_view(), name='fill_loan_request'),
    path('api_test/', APITestView.as_view(), name="api_test")
]