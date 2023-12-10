from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index, name='index'),
    # Add more paths as needed
]