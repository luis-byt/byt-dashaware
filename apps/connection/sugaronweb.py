from django.conf import settings
import mysql.connector


class SugarOnWebError(Exception):
    pass

class SugarOnWebConn(object):
    HOST = settings.SUGARCRM['HOST']
    PORT = settings.SUGARCRM['PORT']
    DATABASE = settings.SUGARCRM['DATABASE']
    USER = settings.SUGARCRM['USER']
    PASSWORD = settings.SUGARCRM['PASSWORD']
    conn = None
    cursor = None

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host = self.HOST,
                user=self.USER,
                password=self.PASSWORD,
                database=self.DATABASE,
                port=self.PORT
            )

            self.cursor = self.conn.cursor()

        except mysql.connector.Error as e:
            print(f"Error al conectar a MySQL: {e}")

    def execute(self, query='SHOW TABLES;'):
        if self.cursor:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        return None

    def close(self):
        self.cursor.close()
        self.cursor = None
        self.conn.close()
        self.conn = None