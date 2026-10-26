
import mysql.connector
from mysql.connector import Error


def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Trabajo1233",
            database="facturacion_alcorte"
        )
        return conexion

    except Error as error:
        print(f"Error al conectar con MySQL: {error}")
        return None
