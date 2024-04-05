from django.urls import path
from .views import Dash

urlpatterns = [
    path('',Dash)
]