import os
import io
import json
from PIL import Image, ImageDraw, ImageFont
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import telegram

# Variáveis de ambiente (Railway)
PASTA_ENTRADA_ID = os.getenv("PASTA_ENTRADA_ID")
PASTA_ESCUDOS_ID = os.getenv("PASTA_ESCUDOS_ID")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Config Google Drive com service account das variáveis
creds_info = json.loads(GOOGLE_CREDENTIALS_JSON)
SCOPES = ['https://www.googleapis.com/auth/drive']
credentials = service_account.Credentials.from_service_account_info(
    creds_info, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)

def baixar_arquivo_drive(file_name, folder_id, output_path):
    query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
    resp = drive_service.files().list(q=query, fields="files(id,name)").execute()
    files = resp.get('files', [])
    if not files:
        raise FileNotFoundError(f"Arquivo '{file_name}' não encontrado na pasta {folder_id}.")
    file_id = files[0]['id']
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(output_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.close()

def gerar_imagem_com_dados():
    os.makedirs("matrizes_oficiais", exist_ok=True)

    base_img = "Matriz Entrada Back Exchange.png"
    caminho_base = f"matrizes_oficiais/{base_img}"
    baixar_arquivo_drive(base_img, PASTA_ENTRADA_ID, caminho_base)

    img = Image.open(caminho_base).convert("RGBA")
    draw = ImageDraw.Draw(img)
    font_path = "arial.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 26)

    # Substitua estes valores por dados reais do Google Sheets
    draw.text((170, 410), "Maracanã", fill="black", font=font)
    draw.text((170, 445), "BRASILEIRÃO", fill="black", font=font)
    draw.text((170, 485), "1.80", fill="black", font=font)
    draw.text((170, 520), "R$ 100", fill="black", font=font)
    draw.text((170, 560), "BACK", fill="black", font=font)
    draw.text((170, 600), "R$ 280", fill="black", font=font)
    draw.text((170, 640), "18:30", fill="black", font=font)
    draw.text((170, 680), "AGUARDANDO", fill="black", font=font)

    esc1 = "flamengo.png"
    esc2 = "palmeiras.png"
    baixar_arquivo_drive(esc1, PASTA_ESCUDOS_ID, esc1)
    baixar_arquivo_drive(esc2, PASTA_ESCUDOS_ID, esc2)

    e1 = Image.open(esc1).convert("RGBA").resize((100, 100))
    e2 = Image.open(esc2).convert("RGBA").resize((100, 100))
    img.paste(e1, (80, 150), e1)
    img.paste(e2, (400, 150), e2)

    output = "matrizes_oficiais/matriz_entrada_preenchida.png"
    img.save(output)
    return output

def enviar_para_telegram(path):
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    with open(path, "rb") as foto:
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=foto)

if __name__ == "__main__":
    try:
        foto = gerar_imagem_com_dados()
        enviar_para_telegram(foto)
        print("✅ Sucesso! Imagem enviada.")
    except Exception as e:
        print("❌ Erro:", e)
