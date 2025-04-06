from django.contrib import admin
from .models import Asset, AssetPrice

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nome', 'limite_superior', 'limite_inferior', 'intervalo_checagem']
    search_fields = ['sigla', 'nome']

@admin.register(AssetPrice)
class AssetPriceAdmin(admin.ModelAdmin):
    list_display = ['ativo', 'preco', 'data_hora']
    list_filter = ['ativo']
