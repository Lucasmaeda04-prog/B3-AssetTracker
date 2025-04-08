from b3monitor.celery import app  
from celery import shared_task
from .models import Asset, AssetPrice
from django.utils import timezone
import yfinance as yf
import logging
from b3monitor.utils import enviar_notificacao_preco
from decimal import Decimal
from datetime import timedelta
logger = logging.getLogger(__name__)

@app.task 
def busca_preco_ativo(asset_id):
    try:
        asset = Asset.objects.get(id=asset_id)
        ticker = yf.Ticker(f"{asset.sigla}.SA")
        current_price = ticker.info.get('regularMarketPrice')
        
        if current_price:
            # Busca o último preço de forma segura
            ultimo_registro = asset.precos.first()
            ultimo_preco = ultimo_registro.preco if ultimo_registro else None
            ultima_data_hora = ultimo_registro.data_hora if ultimo_registro else None
            # Converte o preço atual para Decimal para comparação
            current_price_decimal = Decimal(str(current_price))
            logger.info(f"Preço encontrado para {asset.sigla}: R$ {current_price}")
            
            # Cria novo registro se não existe preço anterior ou se o preço mudou
            if ultimo_preco is None or current_price_decimal != ultimo_preco or timezone.now() < ultima_data_hora + timedelta(minutes=asset.intervalo_checagem):
                    AssetPrice.objects.create(
                        ativo=asset,
                        data_hora=timezone.now(),
                        preco=current_price_decimal
                )
                # Verifica limites e envia notificações
            if current_price_decimal > asset.limite_superior:
                    enviar_notificacao_preco(asset, current_price_decimal, "VENDA")
            elif current_price_decimal < asset.limite_inferior:
                    enviar_notificacao_preco(asset, current_price_decimal, "COMPRA")
            else:
                logger.info(f"Preço não mudou para {asset.sigla}: R$ {current_price}")
        else:
            logger.warning(f"Não foi possível encontrar o preço para {asset.sigla}")
            
    except Exception as e:
        logger.error(f"Erro ao buscar preço para o ativo {asset.sigla}: {str(e)}")

@app.task  
def programa_busca_ativo():
    current_minute = timezone.now().minute
    logger.info(f"Minuto atual: {current_minute}")
    assets = Asset.objects.all()
    
    for asset in assets:
        if current_minute % asset.intervalo_checagem == 0:
            busca_preco_ativo.delay(asset.id)
