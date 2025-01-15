# Module Imports
import sys
import mariadb
# DB1
# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="pi",
        password="flicket",
        host="192.168.1.114",
        port=3306,
        database="employees"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()