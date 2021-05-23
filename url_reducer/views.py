from url_reducer.models import UrlRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse

# Create your views here.
from url_reducer.models import UrlRedirect

def relatorios(requisicao, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    url_reduzida = requisicao.build_absolute_uri(f'/{slug}')
    contexto = {
        'reduce': url_redirect,
        'url_reduzida': url_reduzida,
        }
    return render(requisicao, 'url_reducer/relatorio.html', contexto)


def redirecionar(requisicao, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    return redirect(url_redirect.destino)