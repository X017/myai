from django.urls import path
from .views import OllamaChatView

urlpatterns = [
    path("chat/", OllamaChatView.as_view(), name="chat"),
]
