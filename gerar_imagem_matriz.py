import os
from PIL import Image, ImageDraw, ImageFont
import requests

# Criação do diretório se não existir
output_dir = "matrizes_oficiais"
os.makedirs(output_dir, exist_ok=True)

# Caminhos
input_image_path = os.path.join(output_dir, "Matriz Entrada Back Exchange.png")
output_image_path = os.path.join(output_dir, "matriz_entrada_preenchida.png")

# Variáveis do Telegram (certifique-se que estão configuradas no Railway)
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def gerar_imagem():
    if not os.path.exists(input_image_path):
        print(f"❌ Imagem base não encontrada: {input_image_path}")
        return False

    try:
        imagem_base = Image.open(input_image_path).convert("RGBA")
        draw = ImageDraw.Draw(imagem_base)

        # Fonte
        try:
            fonte = ImageFont.truetype("arial.ttf", 38)
        except:
            fonte = ImageFont.load_default()

        # Dados de exemplo (você pode ajustar depois)
        draw.text((100, 80), "TIME A x TIME B", font=fonte, fill="white")
        draw.text((100, 140), "Horário: 19h30", font=fonte, fill="white")
        draw.text((100, 200), "Estádio: Maracanã", font=fonte, fill="white")

        imagem_base.save(output_image_path)
        print(f"✅ Imagem gerada com sucesso: {output_image_path}")
        return True

    except Exception as e:
        print(f"❌ Erro ao gerar imagem: {e}")
        return False

def enviar_telegram():
    if not os.path.exists(output_image_path):
        print("❌ Arquivo de imagem gerada não encontrado para envio.")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(output_image_path, "rb") as image_file:
        files = {"photo": image_file}
        data = {"chat_id": CHAT_ID}
        response = requests.post(url, files=files, data=data)

    if response.status_code == 200:
        print("✅ Imagem enviada com sucesso para o Telegram.")
    else:
        print(f"❌ Falha no envio para Telegram: {response.status_code} - {response.text}")

if __name__ == "__main__":
    if gerar_imagem():
        enviar_telegram()
