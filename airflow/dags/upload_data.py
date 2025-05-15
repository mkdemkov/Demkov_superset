import datetime
import time

import pandas as pd
import smbclient
from normalize_dpo_regions import Normalizer

from sqlalchemy import create_engine


def upload_contingent(engine):
    programs = smbclient.open_file(
        '\\\\p1c-fs1\\dpobi$\\Слушатели курсов ДПО (XLSX).xlsx',
        mode="rb", encoding='utf-8')

    df = pd.read_excel(io=programs, header=0, decimal=',')
    normalizer = Normalizer('') # апи ключ

    def _apply_norm_iso(region_value):
        if pd.isna(region_value) or str(region_value).strip() == "":
            return pd.Series([None, None], index=['Регион_норм', 'iso_code'])
        result = normalizer.get_normalized_region(region_value)
        return pd.Series([
            result.get('region'),
            result.get('iso_code')
        ], index=['Регион_норм', 'iso_code'])
    
    df[['Регион_норм', 'iso_code']] = (
        df['Регион проживания']
        .apply(_apply_norm_iso)
    )

    df.to_sql(name='Контингент', con=engine, index=False, if_exists='replace')

def upload_programs(engine):
    programs = smbclient.open_file(
        '\\\\p1c-fs1\\dpobi$\\ОП ДПО (ПК+ПП+ДОПВ) (XLSX).xlsx',
        mode="rb", encoding='utf-8')

    df = pd.read_excel(io=programs, header=4, decimal=',')

    df = df.drop(df.columns[[1, 2, 6, 19, 20]], axis=1)

    df.to_sql(name='Программы', con=engine, index=False, if_exists='replace')

def upload_finances(engine):
    programs = smbclient.open_file(
        '\\\\p1c-fs1\\dpobi$\\Платежи и начисления по договорам слушателей (для выгрузки данных в дашборд) (XLSX).xlsx',
        mode="rb", encoding='utf-8')

    df = pd.read_excel(io=programs, header=0, decimal=',')

    df = df.drop(df.columns[[2,3,5,6,7,8,10,11,12,14,15,16,17,18,19,21,23,24,25,26]], axis=1)


    df.to_sql(name='Финансы 1', con=engine, index=False, if_exists='replace')

def upload_excel_tables():
    smbclient.ClientConfig(username='', password='')
    smbclient.register_session(server="p1c-fs1")

    engine = create_engine('')

    print('Start uploading programs')

    upload_programs(engine)

    print('Successfully uploaded programs')

    print('Start uploading finances')

    upload_finances(engine)

    print('Successfully uploaded finances')

    print('Start uploading contingent')

    upload_contingent(engine)

    print('Successfully uploaded contingent')

    smbclient.delete_session(server="p1c-fs1")

while True:
    try:
        print(datetime.datetime.now())
        upload_excel_tables()

        time.sleep(60 * 60 * 3)
    except Exception as e:
        time.sleep(30)
        print(e)