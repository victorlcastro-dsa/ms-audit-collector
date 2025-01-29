import pandas as pd
import xlsxwriter

def save_audit_logs_to_excel(processed_logs):
    final_df = pd.DataFrame(processed_logs)

    # Creating the Excel file
    filename = "Audit_Accounts_Receivable.xlsx"
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")
    final_df.to_excel(writer, sheet_name="Audit", index=False)

    # Styling the Excel file
    workbook = writer.book
    worksheet = writer.sheets["Audit"]

    header_format = workbook.add_format({
        "bold": True, "bg_color": "#4F81BD", "font_color": "white", "border": 1
    })

    for col_num, value in enumerate(final_df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    for i, col in enumerate(final_df.columns):
        max_length = max(final_df[col].astype(str).map(len).max(), len(col)) + 2
        worksheet.set_column(i, i, max_length)

    writer.close()
    print(f"✅ Audit saved in: {filename}")