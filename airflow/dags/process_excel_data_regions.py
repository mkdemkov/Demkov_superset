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


iso_map = {
    "Алтайский край": "RU-ALT",
    "Амурская обл.": "RU-AMU",
    "Архангельская обл.": "RU-ARK",
    "Астраханская обл.": "RU-AST",
    "Белгородская обл.": "RU-BEL",
    "Брянская обл.": "RU-BRY",
    "Владимирская обл.": "RU-VLA",
    "Волгоградская обл.": "RU-VGG",
    "Вологодская обл.": "RU-VLG",
    "Воронежская обл.": "RU-VOR",
    "Еврейская АО": "RU-YEV",
    "Забайкальский край": "RU-ZAB",
    "Ивановская обл.": "RU-IVA",
    "Иркутская обл.": "RU-IRK",
    "Кабардино-Балкарская Республика": "RU-KB",
    "Калининградская обл.": "RU-KGD",
    "Калужская обл.": "RU-KLU",
    "Камчатский край": "RU-KAM",
    "Карачаево-Черкесская Республика": "RU-KC",
    "Кемеровская обл. - Кузбасс": "RU-KEM",  # Officially "Кемеровская область"
    "Кировская обл.": "RU-KIR",
    "Костромская обл.": "RU-KOS",
    "Краснодарский край": "RU-KDA",
    "Красноярский край": "RU-KYA",
    "Курганская обл.": "RU-KGN",
    "Курская обл.": "RU-KRS",
    "Ленинградская обл.": "RU-LEN",
    "Липецкая обл.": "RU-LIP",
    "Магаданская обл.": "RU-MAG",
    "Московская обл.": "RU-MOS",
    "Мурманская обл.": "RU-MUR",
    "Ненецкий АО": "RU-NEN",
    "Нижегородская обл.": "RU-NIZ",
    "Новгородская обл.": "RU-NGR",
    "Новосибирская обл.": "RU-NVS",
    "Омская обл.": "RU-OMS",
    "Оренбургская обл.": "RU-ORE",
    "Орловская обл.": "RU-ORL",
    "Пензенская обл.": "RU-PNZ",
    "Пермский край": "RU-PER",
    "Приморский край": "RU-PRI",
    "Псковская обл.": "RU-PSK",
    "Республика Адыгея (Адыгея)": "RU-AD",
    "Республика Алтай": "RU-AL",
    "Республика Башкортостан": "RU-BA",
    "Республика Бурятия": "RU-BU",
    "Республика Дагестан": "RU-DA",
    "Республика Ингушетия": "RU-IN",
    "Республика Калмыкия": "RU-KL",
    "Республика Карелия": "RU-KR",
    "Республика Коми": "RU-KO",
    # Official ISO 3166-2 does *not* assign RU codes for Crimea/Sevastopol.
    # Use placeholders like "RU-CR" / "RU-SEV" if you want them distinct.
    "Республика Крым": "RU-CR",  # Non-standard
    "Республика Марий Эл": "RU-ME",
    "Республика Мордовия": "RU-MO",
    "Республика Саха (Якутия)": "RU-SA",
    "Республика Северная Осетия - Алания": "RU-SE",
    "Республика Татарстан (Татарстан)": "RU-TA",
    "Республика Тыва": "RU-TY",
    "Республика Хакасия": "RU-KK",
    "Ростовская обл.": "RU-ROS",
    "Рязанская обл.": "RU-RYA",
    "Самарская обл.": "RU-SAM",
    "Саратовская обл.": "RU-SAR",
    "Сахалинская обл.": "RU-SAK",
    "Свердловская обл.": "RU-SVE",
    "Смоленская обл.": "RU-SMO",
    "Ставропольский край": "RU-STA",
    "Тамбовская обл.": "RU-TAM",
    "Тверская обл.": "RU-TVE",
    "Томская обл.": "RU-TOM",
    "Тульская обл.": "RU-TUL",
    "Тюменская обл.": "RU-TYU",
    "Удмуртская Республика": "RU-UD",
    "Ульяновская обл.": "RU-ULY",
    "Хабаровский край": "RU-KHA",
    "Ханты-Мансийский АО - Югра": "RU-KHM",
    "Челябинская обл.": "RU-CHE",
    "Чеченская Республика": "RU-CE",
    "Чувашская Республика - Чувашия": "RU-CU",
    "Чукотский АО": "RU-CHU",
    "Ямало-Ненецкий АО": "RU-YAN",
    "Ярославская обл.": "RU-YAR",
    "г. Москва": "RU-MOW",
    "г. Санкт-Петербург": "RU-SPE",
    "город федерального значения Севастополь": "RU-SEV"  # Non-standard
}


def add_iso_codes_to_excel(
    input_file: str,
    output_file: str,
    region_column: str = "region"
):
    """
    Reads `input_file` (Excel), adds a column `iso_code`,
    and writes the result to `output_file`.
    """
    df = pd.read_excel(input_file)
    
    def get_iso_code(reg_value):
        if pd.isnull(reg_value):
            return None
        reg_value = reg_value.strip()
        return iso_map.get(reg_value, None)  # returns None if not found
    
    df["iso_code"] = df[region_column].apply(get_iso_code)
    
    df.to_excel(output_file, index=False)
    print(f"Successfully wrote updated Excel to {output_file}")

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
    # process_excel()
    input_excel = "data/attenders_processed.xlsx"
    output_excel = "data/attenders_with_iso.xlsx"
    
    add_iso_codes_to_excel(input_excel, output_excel, region_column="region")