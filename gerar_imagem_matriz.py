# gerar_imagem_matriz.py

import os
import sys
from PIL import Image

ESCUDOS_DIR = os.path.join(os.path.dirname(__file__), 'escudos_folder')
PLACEHOLDER = os.path.join(ESCUDOS_DIR, 'placeholder.png')  # icone default

def achar_escudo(nome_time):
    candidato = f"{nome_time}.png"
    caminho = os.path.join(ESCUDOS_DIR, candidato)
    if os.path.isfile(caminho):
        return caminho
    # fallback país: assume formato "nome_time (país).png"
    for arq in os.listdir(ESCUDOS_DIR):
        if arq.lower().startswith(nome_time.lower() + " (") and arq.lower().endswith(").png"):
            return os.path.join(ESCUDOS_DIR, arq)
    return PLACEHOLDER

def gerar_matriz(lista_times, cols, tamanho=(64,64), espacamento=10, cor_fundo=(255,255,255)):
    linhas = (len(lista_times) + cols - 1) // cols
    largura = cols * tamanho[0] + (cols + 1) * espacamento
    altura = linhas * tamanho[1] + (linhas + 1) * espacamento

    img = Image.new('RGB', (largura, altura), cor_fundo)

    for idx, time in enumerate(lista_times):
        caminho = achar_escudo(time)
        escudo = Image.open(caminho).convert('RGBA').resize(tamanho, Image.ANTIALIAS)
        x = espacamento + (idx % cols) * (tamanho[0] + espacamento)
        y = espacamento + (idx // cols) * (tamanho[1] + espacamento)
        img.paste(escudo, (x, y), escudo)

    return img

if __name__ == '__main__':
    # usage: python gerar_imagem_matriz.py times.txt output.png [cols]
    if len(sys.argv) < 3:
        print("Uso: python gerar_imagem_matriz.py lista_times.txt matriz_saida.png [colunas]")
        sys.exit(1)

    lista_arquivo = sys.argv[1]
    saida = sys.argv[2]
    colunas = int(sys.argv[3]) if len(sys.argv) > 3 else 5

    with open(lista_arquivo, encoding='utf-8') as f:
        times = [linha.strip() for linha in f if linha.strip()]

    matriz = gerar_matriz(times, cols=colunas)
    matriz.save(saida)
