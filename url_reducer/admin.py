from url_reducer.models import UrlRedirect
from django.contrib import admin

# Register your models here.

@admin.register(UrlRedirect)
class UrlRedirectAdmin(admin.ModelAdmin):
    list_display = ('destino', 'slug', 'criado_em', 'atualizado_em')
