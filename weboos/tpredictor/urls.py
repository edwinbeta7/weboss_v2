# tpredictor/urls.py

from django.urls import path
from . import views
from .views import *
from asistenteai.views import *
from weboos.views import *
from cumple.views import *

urlpatterns = [
    path('tpredictor/', tpredictor, name='tpredictor'),  # Ruta para la vista principal
    path('cumple/', cumple,name='cumple'), 
    path('asistenteai/', asistenteai, name= 'asistenteai'),
    path('', home, name= 'home'), 
]