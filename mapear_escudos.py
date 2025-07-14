import os
import re
from collections import defaultdict

ESCUDOS_DIR = os.path.join(os.path.dirname(__file__), "ESCUDOS")

def normalizar(nome):
    nome = nome.lower()
    nome = re.sub(r'[^a-z0-9]', '', nome)
    return nome

def mapear_escudos():
    if not os.path.isdir(ESCUDOS_DIR):
        print(f"❌ Pasta não encontrada: {ESCUDOS_DIR}")
        return

    grupos = defaultdict(list)

    for f in os.listdir(ESCUDOS_DIR):
        if not (f.lower().endswith(".png") or f.lower().endswith(".jpg")):
            continue
        nome = os.path.splitext(f)[0]
        key = normalizar(nome)
        grupos[key].append(f)

    with open("escudos_mapeados.txt", "w", encoding="utf-8") as out:
        for key in sorted(grupos.keys()):
            nomes = grupos[key]
            if len(nomes) > 1:
                out.write(f"[DUP] {key}: {nomes}\n")
            else:
                out.write(f"{nomes[0]}\n")

    print("✅ Arquivo gerado: escudos_mapeados.txt")

if __name__ == "__main__":
    mapear_escudos()
