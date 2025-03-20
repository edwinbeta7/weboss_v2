from django.urls import path
from .views import *
from asistenteai.views import *
from weboos.views import *
from tpredictor.views import *

urlpatterns = [
    path('cumple.html', capturar_datos, name='capturar_datos'),
    path('cumple/', cumple,  name='cumple'),
    path('asistenteai/', asistenteai, name= 'asistenteai'),
    path('tpredictor/', tpredictor, name= 'tpredictor'),
    path('', home, name= 'home'),
]