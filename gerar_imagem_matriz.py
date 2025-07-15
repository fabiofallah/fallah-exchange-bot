import os
import io
import cv2
import numpy as np
from googleapiclient.discovery import build
from google.oauth2 import service_account
from telegram import Bot
import logging

logging.basicConfig(level=logging.INFO)

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets.readonly']
CRED_JSON = os.environ['GOOGLE_CREDENTIALS_JSON']
ESCUDOS_FOLDER_ID = os.environ['PASTA_ESCUDOS_ID']
SHEET_ID = os.environ['PASTA_ENTRADA_ID']
MATRIZ_NAME = 'Matriz Entrada Back Exchange.png'
TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT = os.environ['TELEGRAM_CHAT_ID']

creds = service_account.Credentials.from_service_account_info(eval(CRED_JSON), scopes=SCOPES)
drive = build('drive', 'v3', credentials=creds)
sheets = build('sheets', 'v4', credentials=creds)
bot = Bot(TELEGRAM_TOKEN)

def baixar_escudo(nome_time):
    q = f"'{ESCUDOS_FOLDER_ID}' in parents and name contains '{nome_time}'"
    resp = drive.files().list(q=q, fields="files(id,name)").execute()
    files = resp.get('files', [])
    if not files:
        return None
    file = files[0]
    data = drive.files().get_media(fileId=file['id']).execute()
    buf = io.BytesIO(data)
    img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)
    return img

# ... resto do script igual
