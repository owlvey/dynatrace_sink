from datetime import datetime
import mysql.connector

class MySqlGateway:

    def __init__(self, host, user, password, database) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_anchor(self):
        mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database)
        
        try:
            cursor = mydb.cursor()      
            cursor.execute("SELECT end FROM SourceItems order by end desc LIMIT 1")
            result = cursor.fetchall()
            if result:
                return result[0][0]
            else:
                return datetime(2000, 1, 1)

        finally:
            try:
                if cursor:
                    cursor.close()
            finally:
                pass
            mydb.close()       


    def post_entries(self, values: list):
        mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database)
        
        try:
            cursor = mydb.cursor()    
            sql = "INSERT INTO SourceItems (source, start, end, total, availability, experience, latency) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            for val in values:
                cursor.execute(sql, val.to_tuple())  
            mydb.commit()
        finally:
            try:
                if cursor:
                    cursor.close()
            finally:
                pass
            mydb.close()
        
          

        