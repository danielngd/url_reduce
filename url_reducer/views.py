from django.db.models.fields import SlugField
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.db.models.functions import TruncDate
from django.db.models import Count
import string
import random

# Create your views here.
from url_reducer.models import UrlRedirect, Urllog

def home(requisicao):
    return render(requisicao, 'url_reducer/index.html')


def criar_slug(N:int) -> str:

    return ''.join(random.SystemRandom().choice(
        string.ascii_letters + \
        string.digits) for _ in range(N)
    )

def processar(requisicao):
    url = requisicao.POST.get('url')
    url_redirect = UrlRedirect.objects.filter(destino=url)
    if not url_redirect:
        url_redirect = UrlRedirect.objects.create(
            destino = url,
            slug = criar_slug(6)
        )
    else:
        url_redirect = url_redirect[0]
    return redirect('/relatorios/{slug}'.format(slug=url_redirect.slug))

def relatorios(requisicao, slug):
    url_redirect = UrlRedirect.objects.get(slug=slug)
    url_reduzida = requisicao.build_absolute_uri(f'/{slug}')
    redirecionamentos_por_data = list(
            UrlRedirect.objects.filter(
                slug = slug
            ).annotate(
                data = TruncDate('logs__criado_em')
            ).annotate(
                cliques = Count('data')
            ).order_by('data')
    )
    contexto = {
        'reduce': url_redirect,
        'url_reduzida': url_reduzida,
        'redirecionamentos_por_data': redirecionamentos_por_data,
        'total_cliques': sum(r.cliques for r in redirecionamentos_por_data)
        
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
