from conexion import obtener_conexion


def consultar(sql, parametros=()):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute(sql, parametros)
        resultados = cursor.fetchall()
        return resultados

    finally:
        cursor.close()
        conexion.close()


def ejecutar(sql, parametros=()):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(sql, parametros)
        conexion.commit()
        return cursor.lastrowid

    except Exception:
        conexion.rollback()
        raise

    finally:
        cursor.close()
        conexion.close()