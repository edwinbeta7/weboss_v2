from django.urls import path
from cumple.views import *
from weboos.views import *
from .views import *
from tpredictor.views import *

urlpatterns = [
    path('asistenteai/', asistenteai,name='asistenteai'), 
    path('cumple/', cumple,name='cumple'),    
    path('tpredictor/', tpredictor, name= 'tpredictor'),
    path('', home,name='home'),    
]