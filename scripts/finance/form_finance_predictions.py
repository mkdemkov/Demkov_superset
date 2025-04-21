import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing

df = pd.read_excel('data/finance_2024_processed.xlsx')
df['Дата заключения'] = pd.to_datetime(df['Дата заключения'], format='%d.%m.%Y')

df['year'] = df['Дата заключения'].dt.year
revenue = (df
    .groupby(['Уровень программы', 'year'])['Оплачено']
    .sum()
    .reset_index()
)

revenue_pivot = (revenue
    .pivot(index='Уровень программы', columns='year', values='Оплачено')
    .fillna(0)
    .sort_index()
)

years = np.array([2021, 2022, 2023, 2024]).reshape(-1, 1)
forecast_years = np.array([2025, 2026]).reshape(-1, 1)

for col in ['LR_2025','LR_2026','Holt_2025','Holt_2026']:
    revenue_pivot[col] = np.nan

for level, row in revenue_pivot.iterrows():
    ts = row[[2021,2022,2023,2024]].values

    # линейная регрссия
    lr = LinearRegression().fit(years, ts)
    pred_lr = lr.predict(forecast_years)
    revenue_pivot.at[level, 'LR_2025'] = pred_lr[0]
    revenue_pivot.at[level, 'LR_2026'] = pred_lr[1]

    # B) прогноз методом Холта
    holt_model = ExponentialSmoothing(ts, trend='add', seasonal=None,
                                initialization_method="estimated")
    holt = holt_model.fit(optimized=False,
                          smoothing_level=0.8,
                          smoothing_trend=0.2)
    pred_holt = holt.forecast(2)
    revenue_pivot.at[level, 'Holt_2025'] = pred_holt[0]
    revenue_pivot.at[level, 'Holt_2026'] = pred_holt[1]

out = revenue_pivot.reset_index()
out.to_csv('data/finance_forecast.csv', index=False)
