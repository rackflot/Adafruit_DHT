# Module Imports
import sys
import mariadb
# DB1
# Connect to MariaDB Platform

def add_data(time, temp, humid, speed):
    try:
        statement = "INSERT INTO actions(time, temp, humid, speed) VALUES (?,?,?,?)"
        data = (time, temp, humid, speed)
        cursor.execute(statement, data)
        print("successfully added to database")
    except mariadb.Error as e:
       print (f"Error adding entry to databazES {e}") 

def get_data():
    try:
      statement = (f"SELECT * FROM actions")          
      cursor.execute(statement)
      conn.commit()
      # results  =  cursor.fetchall()
      # row = cursor.fetchone()
      for row in cursor.fetchall():
        print (row, sep=' ')
      
    except mariadb.Error as e:
      print(f"Error retrieving entry from database: {e}")


try:
    conn = mariadb.connect(
        user="pi",
        password="flicket",
        host="localhost",
        port=3306,
        database="fan"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cursor = conn.cursor()

add_data(1,2,3,4)
add_data(5,6,7,8)

get_data()


# close it down
cursor.close()
