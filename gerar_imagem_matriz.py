import os
import cv2
import numpy as np
from telegram import Bot
import logging

logging.basicConfig(level=logging.INFO)

# Configurações
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Caminhos
pasta_matriz = 'matrizes_oficiais'
nome_arquivo_matriz = 'Matriz Entrada Back Exchange.png'
caminho_matriz = os.path.join(pasta_matriz, nome_arquivo_matriz)
caminho_escudo = 'escudos/time_teste.png'  # ajuste para o nome do escudo desejado
caminho_saida = os.path.join(pasta_matriz, 'matriz_entrada_preenchida.png')

# Verificação de existência
if not os.path.exists(caminho_matriz):
    logging.error(f"❌ Matriz não encontrada em {caminho_matriz}")
    exit()
if not os.path.exists(caminho_escudo):
    logging.error(f"❌ Escudo não encontrado em {caminho_escudo}")
    exit()

# Carregar matriz
matriz = cv2.imread(caminho_matriz)
altura_matriz, largura_matriz = matriz.shape[:2]

# Carregar escudo
escudo = cv2.imread(caminho_escudo, cv2.IMREAD_UNCHANGED)
escudo = cv2.resize(escudo, (180, 180))  # ajuste de tamanho para caber corretamente

# Inserir escudo na matriz (canto superior esquerdo)
y_offset, x_offset = 420, 150  # ajuste de coordenadas
for c in range(0, 3):
    matriz[y_offset:y_offset+escudo.shape[0], x_offset:x_offset+escudo.shape[1], c] = \
        escudo[:, :, c] * (escudo[:, :, 3]//255) + matriz[y_offset:y_offset+escudo.shape[0], x_offset:x_offset+escudo.shape[1], c] * (1 - escudo[:, :, 3]//255)

# Texto de exemplo para campos
font = cv2.FONT_HERSHEY_SIMPLEX
cor = (0, 0, 0)
espessura = 2
escala = 1.3

cv2.putText(matriz, 'MetLife Stadium', (380, 1280), font, escala, cor, espessura, cv2.LINE_AA)
cv2.putText(matriz, 'FIFA Club WC', (380, 1400), font, escala, cor, espessura, cv2.LINE_AA)
cv2.putText(matriz, '2.44', (380, 1530), font, escala, cor, espessura, cv2.LINE_AA)
cv2.putText(matriz, 'R$ 100', (380, 1660), font, escala, cor, espessura, cv2.LINE_AA)
cv2.putText(matriz, 'Match Odds', (380, 1790), font, escala, cor, espessura, cv2.LINE_AA)
cv2.putText(matriz, '450K', (380, 1920), font, escala, cor, espessura, cv2.LINE_AA)
cv2.putText(matriz, '16:00', (380, 2050), font, escala, cor, espessura, cv2.LINE_AA)
cv2.putText(matriz, 'Aguardando', (380, 2180), font, escala, cor, espessura, cv2.LINE_AA)

cv2.imwrite(caminho_saida, matriz)
logging.info(f"✅ Imagem gerada e salva como {caminho_saida}, pronta para envio ao Telegram.")

# Enviar ao Telegram
with open(caminho_saida, 'rb') as img:
    bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=img)
    logging.info("✅ Imagem enviada ao Telegram com sucesso.")

