from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Asset, AssetPrice
from django.contrib import messages

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['sigla', 'nome', 'limite_superior', 'limite_inferior', 'intervalo_checagem']
    search_fields = ['sigla', 'nome']

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
            messages.success(request, f"Ativo {obj.sigla} salvo com sucesso!")
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                if isinstance(errors, list):
                    for error in errors:
                        form.add_error(field, error)
                else:
                    form.add_error(field, errors)
            messages.error(request, f"Erro ao salvar ativo: {e}")
            return False
        except Exception as e:
            messages.error(request, f"Erro inesperado: {str(e)}")
            return False

@admin.register(AssetPrice)
class AssetPriceAdmin(admin.ModelAdmin):
    list_display = ['ativo', 'preco', 'data_hora']
    list_filter = ['ativo']
