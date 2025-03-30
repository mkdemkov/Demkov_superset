from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

def process_excel(**kwargs):
    import pandas as pd
    
    excel_path = 'data/attenders.xlsx' # файлы поступают в сетевую папку - как поступить на проде ?

    df = pd.read_excel(excel_path)
    
    # Main function to normalize region
    def normalize_region(region):
        region = str(region).lower()
        if 'московск' in region:
            return 'Московская область'
        elif 'москва' in region and 'обл' not in region:
            return 'Москва'
        elif 'перм' in region:
            return 'Пермский край'
        # Other normalization rules
        else:
            return None
    
    # Normalize regions
    df['region_cleaned'] = df['Регион проживания'].apply(normalize_region)
    
    # Foreigners (??)
    df = df[df['region_cleaned'].notnull()]
    
    # Save for the new csv (probably update xlsx or create new one)
    output_path = '/path/to/processed_data.csv'
    df.to_csv(output_path, index=False)
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