import os
import io
import asyncio
from PIL import Image, ImageDraw, ImageFont
from telegram import Bot
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# ==========================
# CONFIGURAÇÕES
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']  # coloque seu chat_id se preferir fixo
PASTA_ENTRADA_ID = '1MRwEUbr3UVZ99BWPpohM5LhGOmU7Mgiz'
ESCUDOS_PASTA_ID = 'COLOQUE_AQUI_O_ID_DA_PASTA_DE_ESCUDOS'
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# ==========================
# AUTENTICAÇÃO DRIVE
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

async def enviar_entrada():
    # Busca arquivo de entrada específico
    file_list = drive.ListFile({'q': f"'{PASTA_ENTRADA_ID}' in parents and trashed=false and title contains 'Matriz Entrada Back Exchange'"}).GetList()
    if not file_list:
        print("❌ Matriz de entrada não encontrada.")
        return
    file_drive = file_list[0]
    file_drive.GetContentFile('entrada_base.png')

    # ABRE A IMAGEM PARA EDIÇÃO
    imagem = Image.open('entrada_base.png').convert('RGB')
    draw = ImageDraw.Draw(imagem)

    # DADOS DA ENTRADA PARA PREENCHER
    confronto = "PSG x Real Madrid"
    estadio = "King Abdullah Sports City"
    competicao = "Super Mundial FIFA"
    odds = "1,85"
    stake = "R$ 100,00"
    mercado = "Back PSG"
    liquidez = "450 K"
    horario = "15:00"
    minutos = "Pré-jogo"

    # CONFIGURAÇÕES DE FONTE
    fonte = ImageFont.truetype("arial.ttf", 48)

    # INSERE TEXTOS NOS CAMPOS (ajuste as coordenadas conforme seu layout)
    draw.text((50, 300), confronto, font=fonte, fill='white')
    draw.text((50, 380), estadio, font=fonte, fill='white')
    draw.text((50, 460), competicao, font=fonte, fill='white')
    draw.text((50, 540), f"Mercado: {mercado}", font=fonte, fill='white')
    draw.text((50, 620), f"Odds: {odds}", font=fonte, fill='white')
    draw.text((50, 700), f"Stake: {stake}", font=fonte, fill='white')
    draw.text((50, 780), f"Liquidez: {liquidez}", font=fonte, fill='white')
    draw.text((50, 860), f"Horário: {horario} ({minutos})", font=fonte, fill='white')

    # SALVA TEMPORÁRIO PARA ENVIO
    imagem.save("entrada_preenchida.png", "PNG")

    # ENVIA AO TELEGRAM
    with open("entrada_preenchida.png", "rb") as img:
        await bot.send_document(chat_id=CHAT_ID, document=img)

    print("✅ Entrada enviada com sucesso ao Telegram.")

if __name__ == '__main__':
    asyncio.run(enviar_entrada())
