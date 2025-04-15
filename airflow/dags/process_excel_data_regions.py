from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import requests
import time

# def process_excel(**kwargs):
#     excel_path = 'data/attenders.xlsx'  # на проде в реальном проекте можно считывать путь из переменных окружения или Airflow Variables
    
#     df = pd.read_excel(excel_path)
    
#     def call_api(region_value):
#         if not region_value or len(region_value) < 2:
#             return None
#         # Здесь укажите ваш реальный IP и порт, где крутится Flask
#         url = "http://192.168.1.135:5000/get_region"
#         try:
#             response = requests.get(url, params={"region": region_value})
#             print(f"Original value - {region_value}, normalized value - {response.text}")
#             time.sleep(3)
#             return response.text
#         except Exception as e:
#             print(f"Ошибка при запросе к API для региона {region_value}: {str(e)}")
#             return None
    
#     # Для каждого региона в «Регион проживания» отправляем запрос на API и записываем ответ в столбец `region`
#     df['region'] = df['Регион проживания'].apply(call_api)
    
#     # Сохраняем результат в новый Excel (или можно перезаписать исходный)
#     output_path = 'data/attenders_processed.xlsx'
#     df.to_excel(output_path, index=False)
#     print(f"Data processed and saved to {output_path}")

regions_normalized = {

}

def process_excel():
    excel_path = 'data/attenders.xlsx'  # на проде в реальном проекте можно считывать путь из переменных окружения или Airflow Variables
    
    df = pd.read_excel(excel_path)
    
    def call_api(region_value):
        if pd.isna(region_value) or not region_value or len(region_value) < 2:
            return None
        if region_value in regions_normalized:
            return regions_normalized[region_value]
        # Здесь укажите ваш реальный IP и порт, где крутится Flask
        url = "http://192.168.1.135:5000/get_region"
        try:
            response = requests.get(url, params={"region": region_value})
            print(f"Original value - {region_value}, normalized value - {response.text}")
            time.sleep(3)
            regions_normalized[region_value] = response.text
            return response.text
        except Exception as e:
            print(f"Ошибка при запросе к API для региона {region_value}: {str(e)}")
            return None
    
    # Для каждого региона в «Регион проживания» отправляем запрос на API и записываем ответ в столбец `region`
    df['region'] = df['Регион проживания'].apply(call_api)
    
    # Сохраняем результат в новый Excel (или можно перезаписать исходный)
    output_path = 'data/attenders_processed.xlsx'
    df.to_excel(output_path, index=False)
    print(f"Data processed and saved to {output_path}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 28),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'process_excel_data',
    default_args=default_args,
    description='Загрузка и обработка еженедельного Excel-файла с данными по регионам слушателей',
    schedule_interval=timedelta(days=7),
)

process_task = PythonOperator(
    task_id='process_excel',
    python_callable=process_excel,
    provide_context=True,
    dag=dag,
)

if __name__ == '__main__':
    process_excel()