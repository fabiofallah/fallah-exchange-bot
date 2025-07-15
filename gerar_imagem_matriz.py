import os
from PIL import Image, ImageDraw, ImageFont
import logging

logging.basicConfig(level=logging.INFO)

def gerar_imagem_matriz():
    # caminhos
    base_path = 'matrizes_oficiais'
    entrada_pra_base = os.path.join(base_path, 'Matriz Entrada Back Exchange.png')
    saida_preenchida = os.path.join(base_path, 'matriz_entrada_preenchida.png')

    # carregar imagem base
    try:
        img = Image.open(entrada_pra_base).convert('RGBA')
        logging.info(f"✅ Base da matriz carregada de '{entrada_pra_base}'.")
    except FileNotFoundError:
        logging.error(f"❌ Imagem base não encontrada: '{entrada_pra_base}'.")
        return False

    draw = ImageDraw.Draw(img)

    # ajustar, se desejar, fonte padrão
    try:
        font = ImageFont.truetype("arial.ttf", size=40)
    except IOError:
        font = ImageFont.load_default()
        logging.warning("⚠️ Fonte Arial não encontrada. Usando fonte padrão.")

    # exemplo: adicionar texto geral (cupom, odds etc.)
    texto = "Entrada: BACK -> LAY"
    pos_texto = (50, 50)
    draw.text(pos_texto, texto, font=font, fill="white")
    logging.info("📝 Adicionado texto na imagem.")

    # exemplo: adicionar escudos de dois times
    escudos_folder = os.environ.get('PASTA_ESCUDOS_ID')
    # OBS: para acessar escudos locais, use caminho correto. Se fizer download, use o nome do arquivo.
    escudos_locais = ['Fluminense.png', 'Flamengo.PNG']
    for i, escudo_nome in enumerate(escudos_locais):
        escudo_caminho = os.path.join(escudos_folder, escudo_nome)
        try:
            esc = Image.open(escudo_caminho).convert('RGBA')
        except Exception as e:
            logging.error(f"❌ Não foi possível abrir escudo {escudo_caminho}: {e}")
            continue

        esc = esc.resize((100, 100), Image.ANTIALIAS)
        pos = (50 + i * 150, 150)
        img.paste(esc, pos, esc)
        logging.info(f"🛡️ Inserido escudo '{escudo_nome}' na posição {pos}.")

    # salvar imagem final
    img.save(saida_preenchida)
    logging.info(f"✅ Imagem salva em '{saida_preenchida}'.")
    return True

# Se executado diretamente
if __name__ == "__main__":
    gerar_imagem_matriz()

