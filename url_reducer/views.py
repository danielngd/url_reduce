from url_reducer.models import UrlRedirect, Urllog
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
    Urllog.objects.create(
    origem = requisicao.META.get('HTTP_REFERER'),
    user_agent = requisicao.META.get('HTTP_USER_AGENT'),
    host = requisicao.META.get('HTTP_HOST'),
    ip = requisicao.META.get('REMOTE_ADDR'),
    url_redirect = url_redirect
    )
    return redirect(url_redirect.destino)