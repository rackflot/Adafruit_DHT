# Module Imports
import sys
import mariadb
from tabulate import tabulate
# DB1
# Connect to MariaDB Platform

class iDHT_DB:
    def __init__(self):
        self.conn = 0
        self.cursor = 0
                
        try:
            self.conn = mariadb.connect(
            user="pi",
            password="flicket",
            host="localhost",
            port=3306,
            database="fan"
        )
            self.cursor = self.conn.cursor()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

# ------------------------------------------------------------------------------

    def print_action_tbl(self):
        sql = "SELECT * FROM actions"
        self.cursor.execute(sql)
        myresult = self.cursor.fetchall()
        print(tabulate(myresult, headers=['time', 'temp', 'humid', 'speed'],tablefmt='psql'))
 # ------------------------------------------------------------------------------       
 
    def add_data(self, time, temp, humid, speed):
        try:
            statement = "INSERT INTO actions(time, temp, humid, speed) VALUES (?,?,?,?)"
            data = (time, temp, humid, speed)
            self.cursor.execute(statement, data)
            print("successfully added to database")
        except mariadb.Error as e:
            print (f"Error adding entry to databases {e}") 
# ------------------------------------------------------------------------------

    def get_data(self):
        try:
            statement = (f"SELECT * FROM actions")          
            self.cursor.execute(statement)
            self.conn.commit()
            # results  =  cursor.fetchall()
            # row = cursor.fetchone()
            for row in self.cursor.fetchall():
                print (row, sep=' ')        
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")

# ------------------------------------------------------------------------------

    def get_columns(self):
        try:
            statement = (f"SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS  WHERE table_name = 'actions';")          
            self.cursor.execute(statement)
            self.conn.commit()
            # results  =  cursor.fetchall()
            # row = cursor.fetchone()
            for row in self.cursor.fetchall():
                print (row, sep=' ')        
        except mariadb.Error as e:
            print(f"Error retrieving entry from database: {e}")
# ------------------------------------------------------------------------------
# test the class
"""
dbh = iDHT_DB()

dbh.print_action_tbl()

dbh.add_data(1,2,3,4)
dbh.add_data(5,6,7,8)

#dbh.get_data()
dbh.get_columns()

dbh.print_action_tbl()

dbh.cursor.close()
"""