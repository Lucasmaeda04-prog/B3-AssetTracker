from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Asset
from .tasks import busca_preco_ativo
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Asset)
def busca_preco_inicial(sender, instance, created, **kwargs):
    if created:
        try:
            result = busca_preco_ativo.delay(instance.id)
        except Exception as e:
            logger.error(f"Erro ao enviar task: {str(e)}")

@receiver(pre_save, sender=Asset)
def atualizar_timestamp(sender, instance, **kwargs):
    instance.atualizado_em = timezone.now()
