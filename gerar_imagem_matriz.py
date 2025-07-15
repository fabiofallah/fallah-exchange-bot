import os
import io
import requests
from PIL import Image, ImageDraw, ImageFont
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import telegram

# Variáveis de ambiente (Railway)
PASTA_ENTRADA_ID = os.getenv("PASTA_ENTRADA_ID")
PASTA_ESCUDOS_ID = os.getenv("PASTA_ESCUDOS_ID")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Autenticação com Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
drive_service = build('drive', 'v3', credentials=credentials)

def baixar_arquivo_drive(file_name, folder_id, output_path):
    query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        raise FileNotFoundError(f"Arquivo '{file_name}' não encontrado na pasta.")
    file_id = items[0]['id']
    request = drive_service.files().get_media(fileId=file_id)
    with io.FileIO(output_path, 'wb') as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()

def gerar_imagem_com_dados():
    print("📥 Baixando matriz base...")
    matriz_path = "matrizes_oficiais/Matriz Entrada Back Exchange.png"
    os.makedirs("matrizes_oficiais", exist_ok=True)
    baixar_arquivo_drive("Matriz Entrada Back Exchange.png", PASTA_ENTRADA_ID, matriz_path)

    print("🖌️ Gerando imagem com dados e escudos...")
    imagem_base = Image.open(matriz_path).convert("RGBA")
    draw = ImageDraw.Draw(imagem_base)

    font_path = "arial.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    fonte = ImageFont.truetype(font_path, 26)

    draw.text((170, 410), "Maracanã", fill="black", font=fonte)
    draw.text((170, 445), "BRASILEIRÃO", fill="black", font=fonte)
    draw.text((170, 485), "1.80", fill="black", font=fonte)
    draw.text((170, 520), "R$ 100", fill="black", font=fonte)
    draw.text((170, 560), "BACK", fill="black", font=fonte)
    draw.text((170, 600), "R$ 280", fill="black", font=fonte)
    draw.text((170, 640), "18:30", fill="black", font=fonte)
    draw.text((170, 680), "AGUARDANDO", fill="black", font=fonte)

    # Baixar escudos
    print("⚽ Inserindo escudos...")
    escudo_time_1_path = "escudo1.png"
    escudo_time_2_path = "escudo2.png"
    baixar_arquivo_drive("flamengo.png", PASTA_ESCUDOS_ID, escudo_time_1_path)
    baixar_arquivo_drive("palmeiras.png", PASTA_ESCUDOS_ID, escudo_time_2_path)

    escudo1 = Image.open(escudo_time_1_path).convert("RGBA").resize((100, 100))
    escudo2 = Image.open(escudo_time_2_path).convert("RGBA").resize((100, 100))

    imagem_base.paste(escudo1, (80, 150), escudo1)
    imagem_base.paste(escudo2, (400, 150), escudo2)

    # Salvar imagem final
    output_image = "matrizes_oficiais/matriz_entrada_preenchida.png"
    imagem_base.save(output_image)
    print("✅ Imagem salva em:", output_image)
    return output_image

def enviar_para_telegram(imagem_path):
    print("🚀 Enviando imagem para o Telegram...")
    bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
    with open(imagem_path, "rb") as f:
        bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=f)
    print("✅ Imagem enviada com sucesso!")

if __name__ == "__main__":
    try:
        img_path = gerar_imagem_com_dados()
        enviar_para_telegram(img_path)
    except Exception as e:
        print(f"❌ Erro: {e}")
