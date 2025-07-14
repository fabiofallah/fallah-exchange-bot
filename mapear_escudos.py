import os
from collections import defaultdict

# Nome da pasta no projeto onde estão os escudos (ajuste conforme necessário)
PASTA_ESCUDOS = "escudos"

# Mapeia os nomes dos arquivos sem a extensão
nomes_escudos = defaultdict(list)

for nome_arquivo in os.listdir(PASTA_ESCUDOS):
    if nome_arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        nome_base = os.path.splitext(nome_arquivo)[0]
        nomes_escudos[nome_base].append(nome_arquivo)

# Cria um relatório dos escudos com nomes repetidos
print("📋 Relatório de escudos com nomes repetidos:\n")
for nome_base, arquivos in nomes_escudos.items():
    if len(arquivos) > 1:
        print(f"🟡 Nome base: '{nome_base}'")
        for arq in arquivos:
            print(f"    ➜ {arq}")
        print()
