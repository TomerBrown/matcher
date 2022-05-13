from django.urls import path
from . import views

urlpatterns = [
    path('', views.find_matches, name='find_matches')
]
