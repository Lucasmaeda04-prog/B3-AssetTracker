from django.db import models
from django.utils import timezone
class Asset(models.Model):
    sigla = models.CharField("Sigla", max_length=10, unique=True, null=True)
    nome = models.CharField("Nome", max_length=100, null=True)
    limite_superior = models.DecimalField("Limite Superior", max_digits=10, decimal_places=2, default=100)
    limite_inferior = models.DecimalField("Limite Inferior", max_digits=10, decimal_places=2, default=0)
    intervalo_checagem = models.IntegerField("Intervalo de Checagem", help_text="Intervalo de checagem em minutos", default=5)
    criado_em = models.DateTimeField("Criado em",default=timezone.now)
    atualizado_em = models.DateTimeField("Atualizado em",default=timezone.now)

    def __str__(self):
        return f"{self.sigla} - {self.nome}"

    class Meta:
        verbose_name = "Ativo"
        verbose_name_plural = "Ativos"

class AssetPrice(models.Model):
    ativo = models.ForeignKey(Asset, verbose_name="Ativo", on_delete=models.CASCADE, related_name='precos', null=True)
    preco = models.DecimalField("Preço", max_digits=10, decimal_places=2, null=True)
    data_hora = models.DateTimeField("Data/Hora",default=timezone.now)

    class Meta:
        ordering = ['-data_hora']
        verbose_name = "Preço do Ativo"
        verbose_name_plural = "Preços dos Ativos"