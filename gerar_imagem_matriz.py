import cv2
import numpy as np
import os

# Caminho da matriz buscada dinamicamente e salva pelo bot
pasta_matriz = 'matrizes_oficiais'
matriz_nome_drive = 'Matriz Entrada Back Exchange.png'  # Nome como chega do Drive
caminho_matriz = os.path.join(pasta_matriz, matriz_nome_drive)

# Nome de saída padronizado para envio ao Telegram
saida_nome = 'matriz_entrada_preenchida.png'
caminho_saida = os.path.join(pasta_matriz, saida_nome)

# Verifica se o arquivo existe antes de prosseguir
if not os.path.exists(caminho_matriz):
    raise FileNotFoundError(f"❌ Arquivo '{caminho_matriz}' não encontrado. Verifique o processo de download do Drive.")

# Carregar a imagem da matriz
matriz = cv2.imread(caminho_matriz)

# Ajustar a largura para 1080 mantendo a proporção para Telegram
altura_original, largura_original = matriz.shape[:2]
escala = 1080 / largura_original
nova_largura = 1080
nova_altura = int(altura_original * escala)
matriz = cv2.resize(matriz, (nova_largura, nova_altura))

# Configuração de fonte e cor
fonte = cv2.FONT_HERSHEY_SIMPLEX
cor_preta = (0, 0, 0)
escala_fonte = 1.1
espessura = 2

# Dados de exemplo (substitua futuramente por variáveis dinâmicas)
estadio = "MetLife Stadium"
competicao = "FIFA Club WC"
odds = "2.44"
stake = "R$ 100"
mercado = "Match Odds"
liquidez = "450K"
horario = "16:00"
resultado = "Aguardando"

# Inserção dos textos nos locais (ajuste conforme necessário)
cv2.putText(matriz, estadio, (90, 1335), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, competicao, (90, 1460), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, odds, (90, 1585), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, stake, (90, 1710), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, mercado, (90, 1835), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, liquidez, (90, 1960), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, horario, (90, 2085), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, resultado, (90, 2210), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)

# Salvar a imagem final no nome padronizado para envio ao Telegram
cv2.imwrite(caminho_saida, matriz)

print(f"✅ Imagem gerada e salva como '{caminho_saida}' pronta para envio ao Telegram.")
