docker system prune --filter "until=168h"
docker exec superset_db psql -U superset -d superset -c "DELETE FROM logs WHERE dttm < now() - interval '90 days';"
