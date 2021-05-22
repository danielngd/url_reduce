from url_reducer.models import UrlRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.

def redirecionar(requisicao, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    return redirect(url_redirect.destino)