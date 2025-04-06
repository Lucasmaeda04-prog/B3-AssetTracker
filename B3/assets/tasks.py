from b3monitor.celery import app  
from celery import shared_task
from .models import Asset, AssetPrice
from django.utils import timezone
import yfinance as yf
import logging

logger = logging.getLogger(__name__)

@app.task 
def busca_preco_ativo(asset_id):
    try:
        asset = Asset.objects.get(id=asset_id)
        logger.info(f"AQUIIIII")
        ticker = yf.Ticker(f"{asset.sigla}.SA")
        current_price = ticker.info.get('regularMarketPrice')
        if current_price:
            AssetPrice.objects.create(
                ativo=asset,
                data_hora=timezone.now(),
                preco=current_price
            )
            logger.info(f"Preço encontrado para {asset.sigla}: R$ {current_price}")
        else:
            logger.warning(f"Não foi possível encontrar o preço para {asset.sigla}")
            
    except Exception as e:
        logger.error(f"Erro ao buscar preço para o ativo {asset.sigla}: {str(e)}")

@app.task  # Use @app.task em vez de @shared_task
def programa_busca_ativo():
    current_minute = timezone.now().minute
    logger.info(f"Minuto atual: {current_minute}")
    assets = Asset.objects.all()
    
    for asset in assets:
        if current_minute % asset.intervalo_checagem == 0:
            busca_preco_ativo.delay(asset.id)
