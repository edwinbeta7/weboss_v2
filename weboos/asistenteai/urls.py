from django.urls import path
from weboos.views import *
from .views import *

urlpatterns = [
    path('asistenteai/', asistenteai,name='asistenteai'), 
    path('', home,name='home'),    
]