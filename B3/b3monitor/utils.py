from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
import logging
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

def enviar_notificacao_preco(ativo, preco, tipo_oportunidade):
    if not ativo.email_alerta:
        logger.warning(f"Ativo {ativo.sigla} não possui email para alertas cadastrado")
        return
    
    subject = f"Oportunidade de {tipo_oportunidade} - {ativo.sigla}"
    
    cor_principal = "#28a745" if tipo_oportunidade == "COMPRA" else "#dc3545"  # Verde para compra, vermelho para venda
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{subject}</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
            .header {{ background-color: {cor_principal}; color: white; padding: 15px; border-radius: 5px; text-align: center; }}
            .content {{ padding: 20px 0; }}
            .price-info {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
            .price-row {{ display: flex; justify-content: space-between; margin: 5px 0; padding: 5px 0; }}
            .footer {{ text-align: center; font-size: 12px; color: #666; margin-top: 20px; border-top: 1px solid #ddd; padding-top: 20px; }}
            .highlight {{ color: {cor_principal}; font-weight: bold; }}
            @media only screen and (max-width: 600px) {{
                .container {{ margin: 10px; padding: 10px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Alerta de {tipo_oportunidade}</h2>
            </div>
            <div class="content">
                <p>Detectamos uma oportunidade de <span class="highlight">{tipo_oportunidade}</span> para o ativo:</p>
                
                <h3>{ativo.sigla} - {ativo.nome}</h3>
                
                <div class="price-info">
    """

    if tipo_oportunidade == "COMPRA":
        diferenca = ativo.limite_inferior - preco
        html_message += f"""
                    <div class="price-row">
                        <strong>Preço Atual:</strong>
                        <span class="highlight">R$ {preco:.2f}</span>
                    </div>
                    <div class="price-row">
                        <strong>Limite Inferior:</strong>
                        <span>R$ {ativo.limite_inferior:.2f}</span>
                    </div>
                    <div class="price-row">
                        <strong>Diferença:</strong>
                        <span class="highlight">R$ {diferenca:.2f} abaixo do limite</span>
                    </div>
        """
    else:  # VENDA
        diferenca = preco - ativo.limite_superior
        html_message += f"""
                    <div class="price-row">
                        <strong>Preço Atual:</strong>
                        <span class="highlight">R$ {preco:.2f}</span>
                    </div>
                    <div class="price-row">
                        <strong>Limite Superior:</strong>
                        <span>R$ {ativo.limite_superior:.2f}</span>
                    </div>
                    <div class="price-row">
                        <strong>Diferença:</strong>
                        <span class="highlight">R$ {diferenca:.2f} acima do limite</span>
                    </div>
        """

    html_message += """
                </div>
                <p>Recomendamos avaliar esta oportunidade de mercado.</p>
            </div>
            <div class="footer">
                <p>Esta é uma mensagem automática do sistema de monitoramento B3.</p>
                <p>Por favor, não responda este email.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Versão em texto simples para clientes que não suportam HTML
    text_message = f"""
    Alerta de {tipo_oportunidade} - {ativo.sigla}
    
    Detectamos uma oportunidade de {tipo_oportunidade} para {ativo.sigla} ({ativo.nome})
    
    Preço Atual: R$ {preco:.2f}
    {'Limite Inferior' if tipo_oportunidade == 'COMPRA' else 'Limite Superior'}: R$ {ativo.limite_inferior if tipo_oportunidade == 'COMPRA' else ativo.limite_superior:.2f}
    Diferença: R$ {diferenca:.2f}
    
    Esta é uma mensagem automática do sistema de monitoramento B3.
    """

    try:
        # Criar o email com múltiplas alternativas
        msg = EmailMultiAlternatives(
            subject=subject,
            body=strip_tags(html_message),  # versão texto extraída do HTML
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[ativo.email_alerta]
        )
        
        # Anexar a versão HTML
        msg.attach_alternative(html_message, "text/html")
        
        # Enviar o email
        msg.send()
        
        logger.info(f"Email de {tipo_oportunidade} enviado com sucesso para {ativo.email_alerta}")
    except Exception as e:
        logger.error(f"Erro ao enviar email para {ativo.email_alerta}: {str(e)}")