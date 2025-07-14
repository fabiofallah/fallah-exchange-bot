import os
import asyncio
from sofascore_wrapper.api import SofascoreAPI
from collections import defaultdict

ESCUDOS_FOLDER = 'escudos'  # pasta com todos os escudos

async def buscar_pais(time: str) -> str:
    api = SofascoreAPI()
    search = await api.search_all(time)
    await api.close()
    if search and search.get('results'):
        entidade = search['results'][0]['entity']
        if entidade.get('team'):
            return entidade['team'].get('slug', '').split('/')[-1]
    return ''

def mapear_escudos():
    arquivos = os.listdir(ESCUDOS_FOLDER)
    base_map = defaultdict(list)
    for f in arquivos:
        nome = f.rsplit('.', 1)[0]
        base_map[nome].append(f)

    duplicates = {k:v for k,v in base_map.items() if len(v)>1}
    simples = {k:v[0] for k,v in base_map.items() if len(v)==1}

    return simples, duplicates

async def escolher_por_pais(duplicates):
    final = {}
    for nome, files in duplicates.items():
        pais = await buscar_pais(nome)
        match = [f for f in files if pais.lower() in f.lower()]
        final[nome] = match[0] if match else files[0]
    return final

def main():
    simples, duplicates = mapear_escudos()
    resultado = dict(simples)
    if duplicates:
        escolhidos = asyncio.run(escolher_por_pais(duplicates))
        resultado.update(escolhidos)
    # Imprima para debug ou retorne
    print("Mapeamento final:", resultado)

if __name__ == '__main__':
    main()
