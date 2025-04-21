import pandas as pd

df = pd.read_csv('data/finance_forecast.csv')

long = df.melt(id_vars=['Уровень программы'],
               value_vars=['2021','2022','2023','2024','LR_2025','LR_2026','Holt_2025','Holt_2026'],
               var_name='year',
               value_name='revenue')

long.to_csv('data/finance_forecast_long.csv', index=False)