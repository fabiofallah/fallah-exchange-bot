# bot.py

import os, io, asyncio, subprocess, logging
from PIL import Image
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials

logging.basicConfig(level=logging.INFO)
ESCUDOS_DIR = 'escudos_folder'
PLACEHOLDER = os.path.join(ESCUDOS_DIR, 'placeholder.png')

def achar_escudo(nome):
    caminho = os.path.join(ESCUDOS_DIR, f"{nome}.png")
    if os.path.isfile(caminho): return caminho
    low = nome.lower()
    for arq in os.listdir(ESCUDOS_DIR):
        n = arq.lower()
        if n.startswith(low + " (") and n.endswith(").png"):
            return os.path.join(ESCUDOS_DIR, arq)
    return PLACEHOLDER

def gerar_matriz(lista):
    cols = 5
    tam = (64,64); esp = 10; bg = (255,255,255)
    linhas = (len(lista)+cols-1)//cols
    w = cols*tam[0] + (cols+1)*esp
    h = linhas*tam[1] + (linhas+1)*esp
    img = Image.new('RGB',(w,h),bg)
    for i,t in enumerate(lista):
        esc = Image.open(achar_escudo(t)).convert('RGBA').resize(tam,Image.ANTIALIAS)
        x = esp + (i%cols)*(tam[0]+esp)
        y = esp + (i//cols)*(tam[1]+esp)
        img.paste(esc,(x,y),esc)
    return img

def baixar_drive(nome, tipo, buf):
    creds = Credentials.from_service_account_info(eval(os.environ['GOOGLE_CREDENTIALS_JSON']))
    svc = build('drive','v3',credentials=creds)
    pid = os.environ[f'PASTA_{tipo}_ID']
    files = svc.files().list(q=f"name='{nome}' and '{pid}' in parents and trashed=false",fields="files(id)").execute().get('files',[])
    if not files: return False
    req = svc.files().get_media(fileId=files[0]['id'])
    dl = MediaIoBaseDownload(buf, req); done = False
    while not done: _, done = dl.next_chunk()
    buf.seek(0); return True

def extrair_times(img):
    # Substitua pela sua lógica de OCR ou leitura de texto
    return ["Time1","Time2","Time3","Time4","Time5"]

async def gerar_entrada(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏳ Processando...")
    buf = io.BytesIO()
    ok = baixar_drive('Matriz Entrada Back Exchange.png','ENTRADA', buf)
    if not ok:
        return await update.message.reply_text("❌ Entrada não encontrada no Drive.")
    img = Image.open(buf)
    times = extrair_times(img)
    matriz = gerar_matriz(times)
    out = io.BytesIO(); matriz.save(out, format='PNG'); out.seek(0)
    await Bot(token=os.environ['TELEGRAM_BOT_TOKEN']).send_photo(chat_id=update.effective_chat.id, photo=out)
    await update.message.reply_text("✅ Entrada processada e enviada.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.environ['TELEGRAM_BOT_TOKEN']).build()
    app.add_handler(CommandHandler('gerarentrada', gerar_entrada))
    app.run_polling()
