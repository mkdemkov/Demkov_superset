import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.holtwinters import ExponentialSmoothing

df = pd.read_excel('data/finance_2024_processed.xlsx')
df['Дата заключения'] = pd.to_datetime(df['Дата заключения'], format='%d.%m.%Y')
df['year'] = df['Дата заключения'].dt.year

top10 = (
    df.groupby('Наименование программы')['Оплачено']
      .sum()
      .nlargest(10)
      .index
)
df = df[df['Наименование программы'].isin(top10)]

years_historic = [2021, 2022, 2023, 2024]
agg = (
    df[df['year'].isin(years_historic)]
    .groupby(['Наименование программы', 'year'])
    .agg(
        Прибыль=('Оплачено', 'sum'),
        Контингент=('Количество слушателей (факт)', 'sum')
    )
    .reset_index()
)

programs = agg['Наименование программы'].unique()
base = pd.MultiIndex.from_product(
    [programs, years_historic],
    names=['Наименование программы', 'year']
).to_frame(index=False)
fact = base.merge(agg, on=['Наименование программы', 'year'], how='left') \
           .fillna(0)

def forecast_linear(ts):
    X = np.array(years_historic).reshape(-1, 1)
    model = LinearRegression().fit(X, ts)
    return model.predict(np.array([2025, 2026]).reshape(-1, 1))

def forecast_holt(ts):
    model = ExponentialSmoothing(
        ts, trend='add', seasonal=None,
        initialization_method="legacy-heuristic"
    ).fit(optimized=True)
    return model.forecast(2)

forecast_years = [2025, 2026]

rows_lr = []
rows_holt = []

for prog in programs:
    sub = fact[fact['Наименование программы'] == prog].sort_values('year')
    profit_ts = sub['Прибыль'].values
    cont_ts   = sub['Контингент'].values

    # линейная регрессия
    pred_p_lr = forecast_linear(profit_ts)
    pred_c_lr = forecast_linear(cont_ts)
    for yr, p, c in zip(forecast_years, pred_p_lr, pred_c_lr):
        rows_lr.append({
            'Наименование программы': prog,
            'Год': yr,
            'Прибыль': p,
            'Контингент': c
        })

    # Холт
    pred_p_h = forecast_holt(profit_ts)
    pred_c_h = forecast_holt(cont_ts)
    for yr, p, c in zip(forecast_years, pred_p_h, pred_c_h):
        rows_holt.append({
            'Наименование программы': prog,
            'Год': yr,
            'Прибыль': p,
            'Контингент': c
        })
df_lr = pd.concat([fact.rename(columns={'year':'Год'}), pd.DataFrame(rows_lr)], ignore_index=True) \
           .sort_values(['Наименование программы','Год'])
df_holt = pd.concat([fact.rename(columns={'year':'Год'}), pd.DataFrame(rows_holt)], ignore_index=True) \
           .sort_values(['Наименование программы','Год'])

df_lr.to_csv('data/forecast_linear.csv', index=False)
df_holt.to_csv('data/forecast_holt.csv', index=False)