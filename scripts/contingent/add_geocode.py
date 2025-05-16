import pandas as pd
import smbclient
from normalize_dpo_regions import Normalizer


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