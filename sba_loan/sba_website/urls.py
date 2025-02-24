from django.urls import path
from .views import HomeView,ClientView, NewsView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('clients_list/', ClientView.as_view(), name='clients_list'),
    path('news_list/', NewsView.as_view(), name='news_list')
]