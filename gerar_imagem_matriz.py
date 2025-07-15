import os
import io
import cv2
import numpy as np
from googleapiclient.discovery import build
from google.oauth2 import service_account
from telegram import Bot
import logging

logging.basicConfig(level=logging.INFO)

# Configurações via variáveis de ambiente
SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets.readonly']
CRED_JSON = os.environ['GOOGLE_CREDENTIALS_JSON']
ESCUDOS_FOLDER_ID = os.environ['PASTA_ESCUDOS_ID']  # garante que esse ID está correto
SHEET_ID = os.environ['PASTA_ENTRADA_ID']
MATRIZ_NAME = 'Matriz Entrada Back Exchange.png'
TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT = os.environ['TELEGRAM_CHAT_ID']

# Inicializa Drive, Sheets e Telegram
creds = service_account.Credentials.from_service_account_info(eval(CRED_JSON), scopes=SCOPES)
drive = build('drive', 'v3', credentials=creds)
sheets = build('sheets', 'v4', credentials=creds)
bot = Bot(TELEGRAM_TOKEN)

def baixar_matriz():
    q = f"'{ESCUDOS_FOLDER_ID}' in parents and name = '{MATRIZ_NAME}'"
    resp = drive.files().list(q=q, fields="files(id)").execute()
    file_id = resp.get('files', [])[0]['id']
    data = drive.files().get_media(fileId=file_id).execute()
    path = MATRIZ_NAME
    with open(path, 'wb') as f: f.write(data)
    return path

def baixar_escudo(nome_time):
    q = f"'{ESCUDOS_FOLDER_ID}' in parents and name contains '{nome_time}'"
    resp = drive.files().list(q=q, fields="files(id,name)").execute()
    files = resp.get('files', [])
    if not files: return None
    data = drive.files().get_media(fileId=files[0]['id']).execute()
    buf = io.BytesIO(data)
    img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)
    return img

def ler_entrada():
    resp = sheets.spreadsheets().values().get(spreadsheetId=SHEET_ID, range='A1:Z1000').execute()
    rows = resp.get('values', [])
    for row in reversed(rows[1:]):
        if len(row) > 13 and row[13].upper() == 'ENTRADA':
            return dict(zip(rows[0], row))
    return None

def gerar_e_enviar():
    entrada = ler_entrada()
    if not entrada:
        logging.error("Nenhuma entrada encontrada.")
        return

    matriz_path = baixar_matriz()
    mat = cv2.imread(matriz_path)
    h, w = mat.shape[:2]

    # Inserir escudos
    for key, pos in [('Time_Casa',(50,300)), ('Time_Visitante',(w-230,300))]:
        img = baixar_escudo(entrada[key])
        if img is not None:
            esc = cv2.resize(img, (180,180))
            x, y = pos
            alpha = esc[:,:,3]/255.0
            for c in range(3):
                mat[y:y+180, x:x+180, c] = (alpha*esc[:,:,c] + (1-alpha)*mat[y:y+180, x:x+180, c])

    # Inserir textos
    font = cv2.FONT_HERSHEY_SIMPLEX
    def put(txt, pos):
        cv2.putText(mat, str(txt), pos, font, 1.2, (0,0,0), 2, cv2.LINE_AA)

    put(entrada['Time_Casa'], (50,500))
    put(entrada['Time_Visitante'], (w-300,500))
    put(entrada['Odds'], (380,600))
    put(entrada['Stake'], (380,650))
    put(entrada['Liquidez'], (50,700))
    put(entrada['Hora'], (50,750))
    put(entrada['Competicao'], (50,800))
    put(entrada['Estadio'], (50,850))

    out = 'matriz_entrada_preenchida.png'
    cv2.imwrite(out, mat)
    bot.send_photo(chat_id=TELEGRAM_CHAT, photo=open(out, 'rb'))
    logging.info("✔️ Entrada enviada.")

if __name__ == '__main__':
    gerar_e_enviar()

