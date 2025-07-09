import os
import json
import io
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Bot

# ========== CONFIGURAÇÃO ==========
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# IDs das planilhas
SPREADSHEET_CLIENTES_ID = "1Frms55KsR5WJ7XUzCvz1CAyjM8P9hna7l2jF9s8EihI"
SPREADSHEET_OPERACOES_ID = "1PJcrAAXa9mDQQm3GtY6vTi05cUUtAALTxVi3vbpM8n8"

# ========== AUTENTICAÇÃO GOOGLE ==========
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = json.loads(os.environ['GOOGLE_CREDENTIALS_JSON'])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
gc = gspread.authorize(creds)

def buscar_chat_id_por_cpf(cpf_robotico):
    sheet = gc.open_by_key(SPREADSHEET_CLIENTES_ID).sheet1
    data = sheet.get_all_records()
    for linha in data:
        if str(linha['CPF_ROBOTICO']) == str(cpf_robotico):
            return linha['CHAT_ID']
    return None

async def verificar_novas_operacoes():
    sheet = gc.open_by_key(SPREADSHEET_OPERACOES_ID).sheet1
    data = sheet.get_all_records()
    for linha in data:
        status = linha['Status'].strip().upper()
        cpf_robotico = linha['CPF_ROBOTICO']
        chat_id = buscar_chat_id_por_cpf(cpf_robotico)

        if not chat_id:
            print(f"❌ CPF Robótico {cpf_robotico} sem cliente correspondente. Ignorado.")
            continue

        if status == "ENTRADA":
            arquivo = "Matriz Entrada Back Exchange.png"  # Ajuste dinâmico futuro conforme operação
            legenda = f"📊 Entrada confirmada para {linha['Time_Casa']} x {linha['Time_Visitante']} às {linha['Hora']} - Odds: {linha['Odds']} - Stake: {linha['Stake']}"
        elif status == "CORRESPONDENCIA":
            arquivo = "Matriz Correspondência Back Exchange.png"
            legenda = f"🔄 Correspondência confirmada para {linha['ID_Operacao']}"
        elif status == "RESULTADO":
            arquivo = "Matriz Resultado Back Exchange.png"
            legenda = f"✅ Resultado: GREEN\nLucro Bruto: {linha['Profit_Bruto']} | Lucro Líquido: {linha['Profit_Liquido']}"
        else:
            print(f"⚠️ Status '{status}' não identificado. Ignorado.")
            continue

        local_file = f"/tmp/{arquivo}"

        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive
        gauth = GoogleAuth()
        gauth.credentials = creds
        drive = GoogleDrive(gauth)

        file_list = drive.ListFile({'q': f"title='{arquivo}' and trashed=false"}).GetList()
        if not file_list:
            print(f"❌ Arquivo '{arquivo}' não encontrado no Drive.")
            continue
        file_drive = file_list[0]
        file_drive.GetContentFile(local_file)

        print(f"📤 Enviando {arquivo} para {chat_id}...")
        with open(local_file, 'rb') as photo:
            await bot.send_document(chat_id=chat_id, document=photo, caption=legenda)
        print("✅ Enviado com sucesso.")

if __name__ == '__main__':
    asyncio.run(verificar_novas_operacoes())
