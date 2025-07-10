import os
from PIL import Image, ImageDraw, ImageFont
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)

def gerar_imagem():
    try:
        # Cria imagem branca
        largura, altura = 1080, 1920
        img = Image.new('RGB', (largura, altura), color='white')
        draw = ImageDraw.Draw(img)

        # Fonte (certifique-se que a fonte existe no ambiente)
        try:
            fonte = ImageFont.truetype("arial.ttf", 60)
        except:
            fonte = ImageFont.load_default()

        # Dados de exemplo (substitua por dados dinâmicos futuramente)
        dados = {
            "Estádio": "MetLife Stadium",
            "Competição": "FIFA Club World Cup",
            "Odds": "2.44",
            "Stake": "R$ 100",
            "Mercado": "Match Odds",
            "Liquidez": "450K",
            "Horário": "16:00",
            "Resultado": "Aguardando"
        }

        # Posições aproximadas
        x, y = 100, 200
        espaco = 100

        for chave, valor in dados.items():
            texto = f"{chave}: {valor}"
            draw.text((x, y), texto, font=fonte, fill='black')
            y += espaco

        # Nome do arquivo e salvamento
        pasta_destino = 'matrizes_oficiais'
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        caminho_arquivo = os.path.join(pasta_destino, 'Matriz Entrada Back Exchange.png')
        img.save(caminho_arquivo)
        logging.info(f"✅ Imagem gerada e salva em '{caminho_arquivo}'")

    except Exception as e:
        logging.error(f"❌ Erro ao gerar imagem: {e}")

if __name__ == '__main__':
    gerar_imagem()
