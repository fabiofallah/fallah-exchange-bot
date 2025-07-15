# gerar_imagem_matriz.py
import os
import io
import cv2
import numpy as np
from googleapiclient.discovery import build
from google.oauth2 import service_account
from telegram import Bot
import logging

logging.basicConfig(level=logging.INFO)

# Configs via variáveis de ambiente
SCOPES = ['https://www.googleapis.com/auth/drive.readonly', 'https://www.googleapis.com/auth/spreadsheets.readonly']
CRED_JSON = os.environ['GOOGLE_CREDENTIALS_JSON']
PASTA_ESCUDOS_ID = os.environ['PASTA_ESCUDOS_ID']
PASTA_ENTRADA_ID = os.environ['PASTA_ENTRADA_ID']
SHEET_ID = os.environ['PASTA_ENTRADA_ID']  # supondo que a pasta de entrada seja a mesma da planilha
MATRIZ_NAME = 'Matriz Entrada Back Exchange.png'
TELEGRAM_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT = os.environ['TELEGRAM_CHAT_ID']

# Autenticação
creds = service_account.Credentials.from_service_account_info(eval(CRED_JSON), scopes=SCOPES)
drive = build('drive', 'v3', credentials=creds)
sheets = build('sheets', 'v4', credentials=creds)
bot = Bot(token=TELEGRAM_TOKEN)

def baixar_matriz():
    logging.info("📥 Iniciando download da matriz do Drive...")
    q = f"'{PASTA_ENTRADA_ID}' in parents and name = '{MATRIZ_NAME}' and trashed = false"
    resp = drive.files().list(q=q, fields='files(id)').execute()
    file_id = resp.get('files', [])[0]['id']
    data = drive.files().get_media(fileId=file_id).execute()
    path = f'matrizes_oficiais/{MATRIZ_NAME}'
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(data)
    logging.info(f"✅ Arquivo '{MATRIZ_NAME}' salvo em '{path}'.")
    return path

def baixar_escudo(time_nome):
    q = f"'{PASTA_ESCUDOS_ID}' in parents and name contains '{time_nome}' and trashed = false"
    resp = drive.files().list(q=q, fields='files(id,name)').execute()
    files = resp.get('files', [])
    if not files:
        return None
    file = files[0]
    data = drive.files().get_media(fileId=file['id']).execute()
    buf = io.BytesIO(data)
    img = cv2.imdecode(np.frombuffer(buf.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)
    return img

def ler_entrada():
    resp = sheets.spreadsheets().values().get(spreadsheetId=SHEET_ID, range='A1:Z1000').execute()
    rows = resp.get('values', [])
    for row in reversed(rows[1:]):
        if len(row) > 13 and row[13].strip().upper() == 'ENTRADA':
            return dict(zip(rows[0], row))
    return None

def gerar_e_enviar():
    entrada = ler_entrada()
    if not entrada:
        logging.error("❌ Nenhuma entrada encontrada.")
        return

    matriz_path = baixar_matriz()
    mat = cv2.imread(matriz_path)
    h, w = mat.shape[:2]

    for key, pos in [('Time_Casa',(50,300)), ('Time_Visitante',(w-230,300))]:
        esc = baixar_escudo(entrada[key])
        if esc is not None:
            esc = cv2.resize(esc, (180,180))
            alpha = esc[:,:,3] / 255.0
            for c in range(3):
                mat[pos[1]:pos[1]+180, pos[0]:pos[0]+180, c] = (
                    alpha * esc[:,:,c] + (1-alpha) * mat[pos[1]:pos[1]+180, pos[0]:pos[0]+180, c]
                )

    font = cv2.FONT_HERSHEY_SIMPLEX
    def put(txt, p):
        cv2.putText(mat, str(txt), p, font, 1.2, (0,0,0), 2, cv2.LINE_AA)

    put(entrada['Time_Casa'], (50,500))
    put(entrada['Time_Visitante'], (w-300,500))
    put(entrada['Odds'], (380,600))
    put(entrada['Stake'], (380,650))
    put(entrada['Liquidez'], (50,700))
    put(entrada['Hora'], (50,750))
    put(entrada['Competicao'], (50,800))
    put(entrada['Estadio'], (50,850))

    out = 'matrizes_oficiais/matriz_entrada_preenchida.png'
    cv2.imwrite(out, mat)

    logging.info("✅ Imagem gerada, enviando ao Telegram...")
    try:
        bot.send_photo(chat_id=TELEGRAM_CHAT, photo=open(out, 'rb'))
        logging.info("✅ Entrada enviada.")
    except Exception as e:
        logging.error(f"❌ Erro no envio ao Telegram: {e}")

if __name__ == '__main__':
    gerar_e_enviar()
