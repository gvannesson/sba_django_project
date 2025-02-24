# chat/urls.py
from django.urls import path

from chat.views import Index_View, Room_View


urlpatterns = [
    path("", Index_View.as_view(), name="index"),
    path("<str:room_name>/", Room_View.as_view(), name="room")
]