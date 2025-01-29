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