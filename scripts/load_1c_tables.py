import json
import re
from pandas import json_normalize
from sqlalchemy import create_engine
import subprocess
import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='/home/vm-admin/superset/docker/.env-non-dev')
JWT= os.getenv("JWT")
POSTGRE_CONNECT = os.getenv("POSTGRE_CONNECT")

def tg_send_msg(bot_msg):
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")
    TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
    send_text = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={TG_CHAT_ID}&text={bot_msg}"
    response = requests.get(send_text)
    return response.json()


def catch_double(match):
    str_escaped = match.group(1).replace("\"", "\\\"")
    str_escaped = str_escaped.replace("\\\"", "\"", 1)
    str_escaped = str_escaped[:-3] + str_escaped[-2:]
    return str_escaped


def load_table(request_name, table_name):
    auth_header = {
        'Authorization': f'Bearer {JWT}'
    }
    response = requests.get(f'http://10.113.0.114:5000/result/get/{request_name}', headers=auth_header)
    inp = json.loads(response.text)

    text = bytes(inp["data"], 'utf-8').decode('unicode_escape')
    text = text.replace("<ComWrapper>", "NULL")
    text = re.sub(r'(: [^:,]*"[^:,]*"[^:,]*"[^:,]*,)', catch_double, text)
    text = json_normalize(json.loads(text))

    ip = subprocess.check_output(
        "docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' superset_db", shell=True,
        text=True).strip()
    engine = create_engine(f'postgresql://{POSTGRE_CONNECT}@{ip}:5432/superset')
    text.to_sql(table_name, engine, if_exists='replace', index=False)
    engine.dispose()

    return len(text)

def main():
    tables = [
        ['superset1', 'запрос_миэм_фактгод_авто'],
        ['superset2', 'запрос_миэм_план_для_лимитов_авто'],
        ['superset_pf4', 'миэм_планфакт_запрос'],
        ['superset_kpi_3', 'миэм_kpi_запрос'],
        ['superset_mixed_op', 'миэм_высшее_обр_запрос'],
        ['superset_nir_3', 'миэм_ниры_запрос'],
        ['superset_limits_ASK_1', 'лимиты_АШК_1'],
        ['superset_limits_ASK_2', 'лимиты_АШК_2'],
    ]
    msg = ""
    for i in tables:
        try:
            res = load_table(i[0], i[1])
            msg += f"{i[0]} успешно, обновлено строк в таблице {i[1]}: {res}\n"
        except Exception as e:
            msg += f"Ошибка импорта запроса {i[0]}: {e}\n"

    tg_send_msg(msg)

if __name__ == '__main__':
    main()

