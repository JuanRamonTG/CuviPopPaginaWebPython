import mysql.connector
from mysql.connector import Error

class crud:
    def __init__(self):
        print("Conectando a la base de datos...")
        self.conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_cuvipop'
        )
        if self.conexion.is_connected():
            print("Conexion exitosa a la base de datos")
        else:
            print("Error al conectar a la base de datos")
        
    def consultar(self, sql):
        cursor = self.conexion.cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()
    
    def ejecutar(self, sql, datos):
        try:
            cursor = self.conexion.cursor()
            cursor.execute(sql, datos)
            self.conexion.commit()
            # devolver número de filas afectadas
            return cursor.rowcount
        except Error as e:
            print(f"Error al ejecutar SQL: {e}")
            return str(e)