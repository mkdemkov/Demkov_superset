#!/bin/bash

GROUP_ID=
BOT_TOKEN=

SCRIPTS_DIR=$(dirname "$(realpath "$0")")
BACKUP_DIR="/home/vm-admin/backups"

BACKUP_FILE="$BACKUP_DIR/backup_`date +%d-%m-%Y"_"%H_%M_%S`.sql"
ARCHIVE_FILE="$BACKUP_DIR/backup_`date +%d-%m-%Y"_"%H_%M_%S`.tar.gz"

docker exec -t superset_db pg_dumpall -c -U superset > "$BACKUP_FILE" 2>&1

if [ $? -eq 0 ]; then
    
    tar -czvf "$ARCHIVE_FILE" --remove-files "$BACKUP_FILE"
    if [ $? -ne 0 ]; then
        RES="Ошибка при создании архива"
    else
        RES="Успешно сохранён дамп базы
Путь: $(realpath "$ARCHIVE_FILE")
Дата: $(date +%Y-%m-%d_%H:%M:%S)
Размер: $(du -h "$ARCHIVE_FILE" | awk '{print $1}')"
    
    fi
else
    RES="Возникла непредвиденная ошибка: $(cat $BACKUP_FILE)"
fi



curl -X POST --data-urlencode "text=$RES" --data-urlencode "chat_id=$GROUP_ID" "https://api.telegram.org/bot$BOT_TOKEN/sendMessage"
