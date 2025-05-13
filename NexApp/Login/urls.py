# myapp/urls.py

from django.urls import path
from . import views 

app_name = 'Login' 

urlpatterns = [
    path('', views.index, name='index'),
]
