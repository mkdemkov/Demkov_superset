## Запуск superset
docker-compose -f docker-compose-non-dev.yml up -d
<br>
/superset/ - основная папка суперсета


## Backup script
Расположение скрипта: superset/scripts/backup.sh
<br>
Скрипт выгружает и сжимает дамп постгре базы, хранящей данные о пользователях, дешбордах, источниках данных. Перед запуском необходимо указать параметры GROUP_ID и BOT_TOKEN.


## Keycloak
https://github.com/apache/superset/discussions/13915
<br>
Для работы требуются:
<br>
/superset/docker/pythonpath_dev/keycloak_security_manager.py - файл, содержащий класс авторизации пользователя, отвечает за login/logout.
<br>
/superset/docker/client_secret.json - файл с параметрами подключения keycloak.
<br>
/superset/docker/pythonpath_dev/superset_config.py - конфигурационный файл суперсета.
<br>
Для keycloak фиксируются параметры OIDC и импортируется класс из keycloak_security_manager.
<br>
/superset/docker/requirements-local.txt - файл с названиями python библиотек, загружаемых при каждом запуске компоуза.
<br>
Для keycloak дополнительно импортируются библиотеки flask-oidc==1.3.0, itsdangerous==2.0.1, flask_openid.


## Перевод
Официальная документация:
<br>
https://superset.apache.org/docs/contributing/translations/
<br>
Для работы требуются:
<br>
/superset/docker/pythonpath_dev/superset_config.py - конфигурационный файл суперсета.
<br>
Для перевода выставляется значение параметра LANGUAGES.
<br>
/superset/superset/translations/messages.pot - хранит список переводимых полей.
<br>
/superset/superset/translations/ru/LC_MESSAGES/messages.po - словарь переводов на русский.
<br>
/superset/superset/translations/ru/LC_MESSAGES/messages.mo - словарь, сконвертированный в бинарный вид.
<br>
/superset/superset/translations/ru/LC_MESSAGES/messages.json - словарь, сконвертированный в json для доступа с фронтенда.