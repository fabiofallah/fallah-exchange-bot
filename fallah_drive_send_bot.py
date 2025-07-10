# Função principal
async def main():
    logger.info("Iniciando envio automático da matriz de ENTRADA com alinhamento corrigido...")

    matriz_nome_drive = "Matriz Entrada Back Exchange.png"
    matriz_nome_local = "matriz_entrada_back_exchange.png"

    matriz_path = baixar_arquivo_drive(matriz_nome_drive, PASTA_ENTRADA_ID, matriz_nome_local)

    if matriz_path:
        logger.info(f"Arquivo {matriz_nome_drive} baixado com sucesso.")
        matriz_preenchida_path = preencher_matriz(matriz_path)

        if os.path.exists(matriz_preenchida_path):
            bot = Bot(token=TELEGRAM_BOT_TOKEN)
            logger.info(f"Enviando a imagem gerada: {matriz_preenchida_path}")
            with open(matriz_preenchida_path, 'rb') as photo:
                await bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo)
            logger.info("Imagem enviada ao Telegram com sucesso.")
        else:
            logger.error(f"Arquivo gerado {matriz_preenchida_path} não encontrado. Envio abortado.")
    else:
        logger.error(f"Arquivo {matriz_nome_drive} não encontrado na pasta do Drive.")


if __name__ == "__main__":
    asyncio.run(main())
