from django.urls import path
from .views import HomeView, DisplayProfileView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('profile/', DisplayProfileView.as_view(), name='display_profile'),
]