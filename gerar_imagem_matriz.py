def gerar_e_enviar():
    entrada = ler_entrada()
    if not entrada:
        logging.error("Nenhuma entrada encontrada.")
        return

    matriz_path = baixar_matriz()
    mat = cv2.imread(matriz_path)
    h, w = mat.shape[:2]

    # insere escudos
    for key, pos in [('Time_Casa', (50,300)), ('Time_Visitante', (w-230,300))]:
        img = baixar_escudo(entrada[key])
        if img is not None:
            esc = cv2.resize(img, (180,180))
            x, y = pos
            alpha = esc[:, :, 3] / 255.0 if esc.shape[2] == 4 else None
            for c in range(3):
                if alpha is not None:
                    mat[y:y+180, x:x+180, c] = (alpha * esc[:, :, c] + (1-alpha) * mat[y:y+180, x:x+180, c])
                else:
                    mat[y:y+180, x:x+180, c] = esc[:, :, c]

    font = cv2.FONT_HERSHEY_SIMPLEX
    def put(txt, pos):
        cv2.putText(mat, str(txt), pos, font, 1.2, (0,0,0), 2, cv2.LINE_AA)

    put(entrada['Time_Casa'], (50,500))
    put(entrada['Time_Visitante'], (w-300,500))
    put(entrada['Odds'], (380,600))
    put(entrada['Stake'], (380,650))
    put(entrada['Liquidez'], (50,700))
    put(entrada['Hora'], (50,750))
    put(entrada['Competicao'], (50,800))
    put(entrada['Estadio'], (50,850))

    out = 'matriz_entrada_preenchida.png'
    cv2.imwrite(out, mat)

    try:
        bot.send_photo(chat_id=TELEGRAM_CHAT, photo=open(out, 'rb'))
        logging.info("✅ Entrada enviada.")
    except Exception as e:
        logging.error(f"❌ Erro no envio ao Telegram: {e}")

if __name__ == '__main__':
    gerar_e_enviar()
