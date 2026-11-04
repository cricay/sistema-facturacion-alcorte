from conexion import obtener_conexion


def consultar(sql, parametros=()):
    conexion = obtener_conexion()

    if conexion is None:
        raise ConnectionError(
            "No fue posible establecer conexión con la base de datos."
        )

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        resultados = cursor.fetchall()
        return resultados

    finally:
        if cursor is not None:
            cursor.close()

        conexion.close()


def ejecutar(sql, parametros=()):
    conexion = obtener_conexion()

    if conexion is None:
        raise ConnectionError(
            "No fue posible establecer conexión con la base de datos."
        )

    cursor = None

    try:
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        conexion.commit()
        return cursor.lastrowid

    except Exception:
        conexion.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()

        conexion.close()