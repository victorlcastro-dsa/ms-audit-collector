import requests
import pandas as pd
from io import StringIO
from msal import ConfidentialClientApplication
import xlsxwriter
from config import Config

# 🔹 Obtendo Token de Acesso
def get_access_token():
    app = ConfidentialClientApplication(Config.CLIENT_ID, authority=Config.AUTHORITY, client_credential=Config.CLIENT_SECRET)
    result = app.acquire_token_for_client(scopes=Config.SCOPE)
    if "access_token" in result:
        print("✅ Token obtido com sucesso!")
        return result["access_token"]
    else:
        raise Exception(f"Erro ao obter token: {result}")

ACCESS_TOKEN = get_access_token()

# 🔹 Obtendo Logs de Atividade do SharePoint
def get_sharepoint_activity_logs():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Accept": "application/json"}
    response = requests.get(Config.ENDPOINT, headers=headers)

    if response.status_code == 403:
        raise Exception("🚨 ERRO: Sem permissão para acessar logs. Verifique no Azure AD se Reports.Read.All foi concedida.")

    response.raise_for_status()

    # Os dados da API são retornados como CSV
    csv_data = response.text
    return pd.read_csv(StringIO(csv_data))

# 🔹 Processando os dados para um formato mais legível
def process_activity_logs(df):
    logs_processados = []

    for _, row in df.iterrows():
        logs_processados.append({
            "Usuário": row.get("User Principal Name", "Desconhecido"),
            "Última Atividade": row.get("Last Activity Date", "Desconhecido"),
            "Arquivos Visualizados/Editados": row.get("Viewed Or Edited File Count", 0),
            "Arquivos Sincronizados": row.get("Synced File Count", 0),
            "Arquivos Compartilhados Internamente": row.get("Shared Internally File Count", 0),
            "Arquivos Compartilhados Externamente": row.get("Shared Externally File Count", 0)
        })

    return logs_processados

# 🔹 Salvando Logs em Excel (Tudo em português)
def save_audit_logs_to_excel():
    print("📊 Coletando logs de atividades do SharePoint...")
    df = get_sharepoint_activity_logs()

    if df.empty:
        print("🚨 Nenhum dado de auditoria encontrado!")
        return

    logs_processados = process_activity_logs(df)
    df_final = pd.DataFrame(logs_processados)

    # Criando o arquivo Excel
    filename = "Auditoria_Contas_a_Receber.xlsx"
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")
    df_final.to_excel(writer, sheet_name="Auditoria", index=False)

    # Estilizando o Excel
    workbook = writer.book
    worksheet = writer.sheets["Auditoria"]

    format_header = workbook.add_format({
        "bold": True, "bg_color": "#4F81BD", "font_color": "white", "border": 1
    })

    for col_num, value in enumerate(df_final.columns.values):
        worksheet.write(0, col_num, value, format_header)

    for i, col in enumerate(df_final.columns):
        max_length = max(df_final[col].astype(str).map(len).max(), len(col)) + 2
        worksheet.set_column(i, i, max_length)

    writer.close()
    print(f"✅ Auditoria salva em: {filename}")

# 🔹 Executando Auditoria
if __name__ == "__main__":
    save_audit_logs_to_excel()