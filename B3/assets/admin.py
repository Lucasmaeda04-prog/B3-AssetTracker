from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Asset, AssetPrice

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nome', 'limite_superior', 'limite_inferior', 'intervalo_checagem']
    search_fields = ['sigla', 'nome']

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                form.add_error(field, errors)
            return 

@admin.register(AssetPrice)
class AssetPriceAdmin(admin.ModelAdmin):
    list_display = ['ativo', 'preco', 'data_hora']
    list_filter = ['ativo']
