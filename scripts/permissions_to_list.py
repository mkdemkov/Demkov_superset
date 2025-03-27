import os
from dotenv import load_dotenv
import psycopg2

load_dotenv('.env-non-dev')

DATABASE_HOST = "localhost" # manually as the script is executed separately
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_DB = os.getenv("DATABASE_DB")


conn_str = f"dbname={DATABASE_DB} user={DATABASE_USER} password={DATABASE_PASSWORD} host={DATABASE_HOST} port={DATABASE_PORT}"

try:
    conn = psycopg2.connect(conn_str)
    cursor = conn.cursor()

    query = """
    SELECT p.name AS permission, vm.name AS view_menu
    FROM ab_permission_view pv
    JOIN ab_permission p ON pv.permission_id = p.id
    JOIN ab_view_menu vm ON pv.view_menu_id = vm.id
    ORDER BY vm.name, p.name;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    with open("available_permissions.txt", "w", encoding="utf-8") as f:
        for permission, view_menu in rows:
            f.write(f"{permission} on {view_menu}\n")

    print("Permissions written to available_permissions.txt")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()