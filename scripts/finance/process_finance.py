import pandas as pd

finance_file = "data/finance_2024.xlsx"
programs_file = "data/programs.xlsx"
output_file = "data/finance_2024_processed.xlsx"

finance_program_col = "Наименование программы"
programs_lookup_col = "НаименованиеОбразовательнойПрограммы"
status_col = "Статус заключения"
paid_col = "Оплачено"
valid_statuses = ["Утвержден", "Закрыт"]
level_col = "Уровень программы"

df_fin = pd.read_excel(finance_file)
df_prog = pd.read_excel(programs_file)

df_fin.columns = df_fin.columns.str.strip()
df_prog.columns = df_prog.columns.str.strip()

required_fin = [finance_program_col, status_col, paid_col]
required_prog = [programs_lookup_col, level_col]
for col in required_fin:
    if col not in df_fin.columns:
        raise KeyError(f"Column '{col}' not found in finance file. Available: {df_fin.columns.tolist()}")
for col in required_prog:
    if col not in df_prog.columns:
        raise KeyError(f"Column '{col}' not found in programs file. Available: {df_prog.columns.tolist()}")

df_fin[finance_program_col] = df_fin[finance_program_col].astype(str).str.strip()
df_fin = df_fin[df_fin[finance_program_col].ne("")]

df_fin = df_fin[df_fin[status_col].isin(valid_statuses)]

df_prog[programs_lookup_col] = df_prog[programs_lookup_col].astype(str).str.strip()

df_prog = df_prog.drop_duplicates(subset=[programs_lookup_col], keep='first')

df_lookup = (
    df_prog[[programs_lookup_col, level_col]]
    .rename(columns={programs_lookup_col: finance_program_col})
)

df_merged = df_fin.merge(df_lookup, on=finance_program_col, how="left")

mask_program = (
    df_merged[finance_program_col].notna() &
    df_merged[finance_program_col].astype(str).str.strip().str.lower().ne("nan")
)
df_merged = df_merged[mask_program]
mask_paid = (
    df_merged[paid_col].notna() &
    df_merged[paid_col].astype(str).str.strip().ne("")
)
df_merged = df_merged[mask_paid]

deficit = df_merged[level_col].isna().sum()
if deficit:
    print(f"Warning: {deficit} finance row(s) could not find a matching program level.")


df_merged.to_excel(output_file, index=False)
print(f"Done! Enriched finance saved to '{output_file}'")