import os
import io
import json
import requests
from PIL import Image, ImageDraw, ImageFont
from google.oauth2 import service_account
from googleapiclient.discovery import build
from telegram import Bot

# === VARIÁVEIS DE AMBIENTE ===
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['CHAT_ID']
DRIVE_FOLDER_ID = os.environ['DRIVE_FOLDER_ID']

# === DADOS DA MATRIZ ===
DADOS_TEXTO = {
    'ESTÁDIO': 'Maracanã',
    'COMPETIÇÃO': 'Brasileirão Série A',
    'ODDS': '1.90',
    'STAKE': 'R$100',
    'MERCADO': 'Back FT',
    'LIQUIDEZ': 'Alta',
    'HORÁRIO': '16:00',
    'RESULTADO': '',
}

# === AUTENTICAÇÃO COM GOOGLE DRIVE ===
def autenticar_drive():
    info = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
    credenciais = service_account.Credentials.from_service_account_info(
        info, scopes=['https://www.googleapis.com/auth/drive']
    )
    return build('drive', 'v3', credentials=credenciais)

# === BUSCA A IMAGEM NA PASTA ===
def buscar_imagem_matriz(service):
    resultados = service.files().list(
        q=f"'{DRIVE_FOLDER_ID}' in parents and mimeType='image/png'",
        fields="files(id, name)"
    ).execute()
    arquivos = resultados.get('files', [])
    if not arquivos:
        raise Exception("Nenhuma imagem PNG encontrada na pasta ENTRADA.")
    return arquivos[0]['id'], arquivos[0]['name']

# === DOWNLOAD DA IMAGEM ===
def baixar_imagem(service, file_id):
    buffer = io.BytesIO()
    resposta = requests.get(
        f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media',
        headers={"Authorization": f"Bearer {service._http.credentials.token}"}
    )
    buffer.write(resposta.content)
    buffer.seek(0)
    return Image.open(buffer).convert('RGB')

# === ESCREVE OS DADOS NA IMAGEM ===
def preencher_imagem(imagem, dados):
    draw = ImageDraw.Draw(imagem)
    font = ImageFont.load_default()

    draw.text((60, 430), f"🏟️ ESTÁDIO : {dados['ESTÁDIO']}", font=font, fill='black')
    draw.text((60, 460), f"🏆 COMPETIÇÃO : {dados['COMPETIÇÃO']}", font=font, fill='black')
    draw.text((60, 490), f"💸 ODDS : {dados['ODDS']}", font=font, fill='black')
    draw.text((60, 520), f"📌 STAKE : {dados['STAKE']}", font=font, fill='black')
    draw.text((60, 550), f"📊 MERCADO : {dados['MERCADO']}", font=font, fill='black')
    draw.text((60, 580), f"💧 LIQUIDEZ : {dados['LIQUIDEZ']}", font=font, fill='black')
    draw.text((60, 610), f"🕒 HORÁRIO : {dados['HORÁRIO']}", font=font, fill='black')
    draw.text((60, 640), f"✅ RESULTADO : {dados['RESULTADO']}", font=font, fill='black')

    return imagem

# === ENVIA A IMAGEM VIA TELEGRAM ===
def enviar_para_telegram(imagem):
    bot = Bot(token=TELEGRAM_TOKEN)
    buffer = io.BytesIO()
    imagem.save(buffer, format='PNG')
    buffer.seek(0)
    bot.send_photo(chat_id=CHAT_ID, photo=buffer, caption="✅ Entrada gerada automaticamente")

# === EXECUÇÃO ===
def main():
    print("🚀 Iniciando robô...")

    try:
        service = autenticar_drive()
        file_id, nome = buscar_imagem_matriz(service)
        print(f"🖼️ Imagem encontrada: {nome}")
        imagem = baixar_imagem(service, file_id)
        imagem_editada = preencher_imagem(imagem, DADOS_TEXTO)
        enviar_para_telegram(imagem_editada)
        print("✅ Entrada enviada com sucesso!")
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")

if __name__ == '__main__':
    main()
