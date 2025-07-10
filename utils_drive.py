def baixar_arquivo_drive(nome_arquivo, tipo_operacao, destino):
    try:
        creds_json = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        creds_dict = eval(creds_json)
        creds = service_account.Credentials.from_service_account_info(creds_dict)

        service = build('drive', 'v3', credentials=creds)

        pasta_drive_map = {
            "ENTRADA": os.environ.get('PASTA_ENTRADA_ID'),
            "CORRESPONDENCIA": os.environ.get('PASTA_CORRESPONDENCIA_ID'),
            "RESULTADO": os.environ.get('PASTA_RESULTADO_ID'),
            "CONECAO": os.environ.get('PASTA_CONEXAO_ID'),
            "AFRICA": os.environ.get('PASTA_AFRICA_ID'),
            "AMERICA": os.environ.get('PASTA_AMERICA_ID'),
            "ASIA": os.environ.get('PASTA_ASIA_ID'),
            "EUROPA": os.environ.get('PASTA_EUROPA_ID'),
            "BANDEIRAS": os.environ.get('PASTA_BANDEIRAS_ID')
        }

        pasta_id = pasta_drive_map.get(tipo_operacao.upper())
        if not pasta_id:
            logging.error(f"❌ Tipo de operação '{tipo_operacao}' não encontrado no mapeamento.")
            return None

        query = f"name='{nome_arquivo}' and '{pasta_id}' in parents and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            logging.error(f"❌ Arquivo '{nome_arquivo}' não encontrado na pasta de {tipo_operacao}.")
            return None

        file_id = items[0]['id']

        # 🚩 CRIA A PASTA AUTOMATICAMENTE SE NÃO EXISTIR
        pasta_destino = os.path.dirname(destino)
        if pasta_destino and not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino, exist_ok=True)
            logging.info(f"📂 Pasta '{pasta_destino}' criada automaticamente.")

        request = service.files().get_media(fileId=file_id)
        fh = io.FileIO(destino, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                logging.info(f"⬇️ Download {int(status.progress() * 100)}% concluído.")

        logging.info(f"✅ Arquivo '{nome_arquivo}' baixado como '{destino}'.")
        return destino

    except Exception as e:
        logging.error(f"❌ Erro ao baixar arquivo do Drive: {e}")
        return None
