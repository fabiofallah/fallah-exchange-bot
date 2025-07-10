import cv2
import numpy as np

# Carregar a imagem da matriz original (sem compressão)
matriz = cv2.imread('/app/matrizes_oficiais/Matriz Entrada Back Exchange.png')

# Ajustar a largura para 1080 mantendo a proporção (Telegram)
altura_original, largura_original = matriz.shape[:2]
escala = 1080 / largura_original
nova_largura = 1080
nova_altura = int(altura_original * escala)
matriz = cv2.resize(matriz, (nova_largura, nova_altura))

# Configuração de fonte e cor
fonte = cv2.FONT_HERSHEY_SIMPLEX
cor_preta = (0, 0, 0)
cor_branca = (255, 255, 255)

# Dados de exemplo (substitua pelos dados do evento)
estadio = "MetLife Stadium"
competicao = "FIFA Club WC"
odds = "2.44"
stake = "R$ 100"
mercado = "Match Odds"
liquidez = "450K"
horario = "16:00"
resultado = "Aguardando"

# Escala da fonte e espessura
escala_fonte = 1.1
espessura = 2

# Coordenadas mapeadas a partir do seu Canva (ajustadas milimetricamente)
cv2.putText(matriz, estadio, (90, 1335), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, competicao, (90, 1460), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, odds, (90, 1585), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, stake, (90, 1710), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, mercado, (90, 1835), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, liquidez, (90, 1960), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, horario, (90, 2085), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)
cv2.putText(matriz, resultado, (90, 2210), fonte, escala_fonte, cor_preta, espessura, cv2.LINE_AA)

# Salvar a imagem final pronta para o Telegram
cv2.imwrite('matriz_entrada_preenchida.png', matriz)

print("✅ Imagem gerada com alinhamento exato e salva como 'matriz_entrada_preenchida.png'")
