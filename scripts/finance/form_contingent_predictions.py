import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_excel('data/finance_2024_processed.xlsx')
df['Дата заключения'] = pd.to_datetime(df['Дата заключения'], format='%d.%m.%Y')
df['year'] = df['Дата заключения'].dt.year

att = (
    df.groupby(['Уровень программы', 'year'])['Количество слушателей (факт)']
      .sum()
      .reset_index()
      .rename(columns={'Количество слушателей (факт)': 'attenders'})
)

years = [2021, 2022, 2023, 2024]
att_wide = att.pivot(index='Уровень программы', columns='year', values='attenders') \
              .reindex(columns=years, fill_value=0)
att_wide = att_wide.fillna(0)

forecast_list = []
X = np.array(years).reshape(-1, 1)
for level, row in att_wide.iterrows():
    y = row.values
    model = LinearRegression().fit(X, y)
    for yr in [2025, 2026]:
        pred = model.predict(np.array([[yr]]))[0]
        forecast_list.append({
            'Уровень программы': level,
            'year': yr,
            'attenders': pred
        })

forecast_df = pd.DataFrame(forecast_list)
long_df = pd.concat([att, forecast_df], ignore_index=True)
long_df = long_df.sort_values(['Уровень программы', 'year'])

output_path = 'data/finance_attenders_long.csv'
long_df.to_csv(output_path, index=False)
