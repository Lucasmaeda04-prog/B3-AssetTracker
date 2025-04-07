from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def enviar_notificacao_preco(ativo, preco, tipo_oportunidade):
    """
    Envia email para superusuários sobre oportunidades de compra/venda
    """
    User = get_user_model()
    superusers = User.objects.filter(is_superuser=True)
    
    if not superusers.exists():
        logger.warning("Nenhum superusuário encontrado para enviar notificação")
        return
    
    subject = f"Oportunidade de {tipo_oportunidade} - {ativo.sigla}"
    
    if tipo_oportunidade == "COMPRA":
        message = (
            f"Oportunidade de COMPRA detectada para {ativo.sigla} ({ativo.nome})\n\n"
            f"Preço Atual: R$ {preco}\n"
            f"Limite Inferior: R$ {ativo.limite_inferior}\n"
            f"Diferença: R$ {ativo.limite_inferior - preco}\n\n"
            f"Esta é uma mensagem automática do sistema de monitoramento."
        )
    else:  # VENDA
        message = (
            f"Oportunidade de VENDA detectada para {ativo.sigla} ({ativo.nome})\n\n"
            f"Preço Atual: R$ {preco}\n"
            f"Limite Superior: R$ {ativo.limite_superior}\n"
            f"Diferença: R$ {preco - ativo.limite_superior}\n\n"
            f"Esta é uma mensagem automática do sistema de monitoramento."
        )

    recipient_list = [user.email for user in superusers]
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        logger.info(f"Email de {tipo_oportunidade} enviado com sucesso para {', '.join(recipient_list)}")
    except Exception as e:
        logger.error(f"Erro ao enviar email: {str(e)}")