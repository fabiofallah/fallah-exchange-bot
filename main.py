import os
import io
import requests
from PIL import Image, ImageDraw, ImageFont
from google.oauth2 import service_account
from googleapiclient.discovery import build
from telegram import Bot

# === CONFIGURAÇÃO DO TELEGRAM ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # CHAT_ID de teste fixo

# === CONFIGURAÇÃO DO GOOGLE DRIVE ===
DRIVE_FOLDER_ID = os.environ.get("PASTA_ENTRADA_ID")

# === CREDENCIAIS DA CONTA DE SERVIÇO ===
import json
google_credentials_dict = json.loads(os.environ.get("GOOGLE_CREDENTIALS_JSON"))
credentials = service_account.Credentials.from_service_account_info(
    google_credentials_dict,
    scopes=["https://www.googleapis.com/auth/drive"]
)

# === DADOS DE EXEMPLO PARA INSERIR NA MATRIZ ===
DADOS_TEXTO = {
    'ESTÁDIO': 'Maracanã',
    'COMPETIÇÃO': 'Brasileirão Série A',
    'ODDS': '1.90',
    'TIME CASA': 'Fluminense',
    'TIME VISITANTE': 'Flamengo',
    'HORÁRIO': '16:00',
}

# === AUTENTICAÇÃO COM GOOGLE DRIVE ===
def autenticar_drive():
    return build('drive', 'v3', credentials=credentials)

# === BUSCA A PRIMEIRA IMAGEM PNG NA PASTA DE ENTRADA ===
def buscar_imagem_matriz(service):
    resultados = service.files().list(
        q=f"'{DRIVE_FOLDER_ID}' in parents and mimeType='image/png'",
        orderBy="createdTime desc",
        fields="files(id, name)"
    ).execute()
    arquivos = resultados.get('files', [])
    if not arquivos:
        raise Exception("Nenhuma imagem PNG encontrada na pasta ENTRADA.")
    return arquivos[0]['id'], arquivos[0]['name']

# === FAZ O DOWNLOAD DA IMAGEM PARA MEMÓRIA ===
def baixar_imagem(file_id):
    token = credentials.token
    if not token:
        credentials.refresh(requests.Request())
        token = credentials.token

    resposta = requests.get(
        f'https://www.googleapis.com/drive/v3/files/{file_id}?alt=media',
        headers={"Authorization": f"Bearer {token}"}
    )

    if resposta.status_code != 200:
        raise Exception("Erro ao baixar a imagem do Drive.")

    buffer = io.BytesIO(resposta.content)
    buffer.seek(0)
    return Image.open(buffer).convert('RGB')

# === ESCREVE OS DADOS NA IMAGEM ===
def preencher_imagem(imagem, dados):
    draw = ImageDraw.Draw(imagem)
    font = ImageFont.truetype("arial.ttf", 28)

    draw.text((50, 430), f"🏟️ ESTÁDIO: {dados['ESTÁDIO']}", font=font, fill='black')
    draw.text((50, 470), f"🏆 COMPETIÇÃO: {dados['COMPETIÇÃO']}", font=font, fill='black')
    draw.text((50, 510), f"💸 ODDS: {dados['ODDS']}", font=font, fill='black')
    draw.text((50, 550), f"🏠 {dados['TIME CASA']} x {dados['TIME VISITANTE']}", font=font, fill='black')
    draw.text((50, 590), f"🕒 HORÁRIO: {dados['HORÁRIO']}", font=font, fill='black')

    return imagem

# === ENVIA A IMAGEM PARA O TELEGRAM ===
def enviar_para_telegram(imagem):
    bot = Bot(token=TELEGRAM_TOKEN)
    buffer = io.BytesIO()
    imagem.save(buffer, format='PNG')
    buffer.seek(0)
    bot.send_photo(chat_id=CHAT_ID, photo=buffer, caption="✅ Entrada gerada automaticamente")

# === FLUXO PRINCIPAL ===
def main():
    print("🚀 Iniciando robô...")

    try:
        service = autenticar_drive()
        file_id, nome = buscar_imagem_matriz(service)
        print(f"🖼️ Imagem encontrada: {nome}")
        imagem = baixar_imagem(file_id)
        imagem_editada = preencher_imagem(imagem, DADOS_TEXTO)
        enviar_para_telegram(imagem_editada)
        print("✅ Entrada enviada com sucesso!")

    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")

if __name__ == '__main__':
    main()
