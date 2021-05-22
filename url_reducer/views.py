from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.

def redirecionar(requisicao, slug):
    return redirect('http://google.com')