from django.shortcuts import render
from django.views import View

# Create your views here.
def home(request):
    #codigo
    return render(request, 'home.html')
