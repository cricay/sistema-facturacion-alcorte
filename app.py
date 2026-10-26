
from flask import (
    Flask, render_template, render_template_string,
    request, redirect, url_for, flash
)
from conexion import obtener_conexion
from werkzeug.security import generate_password_hash
from markupsafe import escape

app = Flask(__name__)
app.secret_key = "alcorte_clave_local_2026"



def pagina(titulo, contenido):
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{{ titulo }} - AL CORTE</title>
        <style>
            body {
                font-family: Arial;
                margin: 30px;
                background: #f5f5f5;
                color: #333;
            }

            h1 {
                color: #651c2a;
            }

            nav a {
                margin-right: 15px;
                color: #651c2a;
                font-weight: bold;
            }

            .contenedor {
                background: white;
                padding: 22px;
                border-radius: 8px;
            }

            input, select {
                display: block;
                width: 95%;
                padding: 10px;
                margin: 8px 0 15px;
            }

            button {
                background: #651c2a;
                color: white;
                padding: 10px 18px;
                border: 0;
                cursor: pointer;
            }

            table {
                border-collapse: collapse;
                width: 100%;
                margin-top: 20px;
            }

            th, td {
                border: 1px solid #ddd;
                padding: 10px;
                text-align: left;
            }

            th {
                background: #651c2a;
                color: white;
            }

            .mensaje {
                padding: 10px;
                background: #eee;
                margin: 10px 0;
            }
        </style>
    </head>

    <body>
        <h1>Sistema de Facturación AL CORTE</h1>

        <nav>
            <a href="/">Inicio</a>
            <a href="/productos">Productos</a>
            <a href="/clientes">Clientes</a>
            <a href="/categorias">Categorías</a>
            <a href="/usuarios">Usuarios</a>
            <a href="/inventario">Inventario</a>
        </nav>

        <hr>

        <div class="contenedor">
            <h2>{{ titulo }}</h2>

            {% for categoria, mensaje in get_flashed_messages(with_categories=true) %}
                <div class="mensaje">{{ mensaje }}</div>
            {% endfor %}

            {{ contenido|safe }}
        </div>
    </body>
    </html>
    """, titulo=titulo, contenido=contenido)



def consultar(sql, parametros=()):
    conexion = obtener_conexion()
    if conexion is None:
        raise Exception("No se pudo conectar con MySQL.")

    cursor = None
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.execute(sql, parametros)
        return cursor.fetchall()
    finally:
        if cursor:
            cursor.close()
        conexion.close()


def ejecutar(sql, parametros=()):
    conexion = obtener_conexion()
    if conexion is None:
        raise Exception("No se pudo conectar con MySQL.")

    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        conexion.close()


@app.route("/")
def inicio():
    return render_template("inicio.html")


# ---------------- PRODUCTOS ----------------

@app.route("/productos")
def listar_productos():
    try:
        productos = consultar("""
            SELECT idProducto, codigo, nombre, precio,
                   unidadMedida, stockMinimo, estado, idCategoria
            FROM productos
            ORDER BY nombre
        """)
        return render_template("productos/lista.html", productos=productos)
    except Exception as error:
        return f"Error al consultar productos: {escape(error)}", 500


@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    if request.method == "POST":
        try:
            ejecutar("""
                INSERT INTO productos
                    (codigo, nombre, precio, unidadMedida,
                     stockMinimo, estado, idCategoria)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                request.form["codigo"].strip(),
                request.form["nombre"].strip(),
                request.form["precio"],
                request.form["unidadMedida"],
                request.form["stockMinimo"],
                request.form["estado"],
                request.form["idCategoria"]
            ))
            flash("Producto registrado correctamente.")
            return redirect(url_for("listar_productos"))
        except Exception as error:
            return f"Error al registrar producto: {escape(error)}", 500

    try:
        categorias = consultar("""
            SELECT idCategoria, nombreCategoria
            FROM categorias ORDER BY nombreCategoria
        """)
        return render_template("productos/nuevo.html", categorias=categorias)
    except Exception as error:
        return f"Error al consultar categorías: {escape(error)}", 500


# ---------------- CLIENTES ----------------

@app.route("/clientes")
def listar_clientes():
    try:
        clientes = consultar("""
            SELECT idCliente, documento, nombre, telefono, direccion, correo
            FROM clientes ORDER BY nombre
        """)

        filas = "".join(
            "<tr>" +
            "".join(f"<td>{escape(str(c.get(k) or ''))}</td>" for k in
                    ["idCliente", "documento", "nombre", "telefono", "direccion", "correo"]) +
            "</tr>"
            for c in clientes
        )

        contenido = """
        <a href="/clientes/nuevo">+ Registrar cliente</a>
        <table><tr><th>ID</th><th>Documento</th><th>Nombre</th>
        <th>Teléfono</th><th>Dirección</th><th>Correo</th></tr>
        """ + filas + "</table>"

        return pagina("Gestión de clientes", contenido)
    except Exception as error:
        return f"Error al consultar clientes: {escape(error)}", 500


@app.route("/clientes/nuevo", methods=["GET", "POST"])
def nuevo_cliente():
    if request.method == "POST":
        try:
            ejecutar("""
                INSERT INTO clientes
                    (documento, nombre, telefono, direccion, correo)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                request.form["documento"].strip(),
                request.form["nombre"].strip(),
                request.form.get("telefono", "").strip() or None,
                request.form.get("direccion", "").strip() or None,
                request.form.get("correo", "").strip() or None
            ))
            flash("Cliente registrado correctamente.")
            return redirect(url_for("listar_clientes"))
        except Exception as error:
            return f"Error al registrar cliente: {escape(error)}", 500

    contenido = """
    <form method="POST">
        <label>Documento *</label><input name="documento" maxlength="20" required>
        <label>Nombre completo *</label><input name="nombre" maxlength="120" required>
        <label>Teléfono</label><input name="telefono" maxlength="20">
        <label>Dirección</label><input name="direccion" maxlength="150">
        <label>Correo</label><input type="email" name="correo" maxlength="120">
        <button type="submit">Guardar cliente</button>
    </form>
    """
    return pagina("Registrar cliente", contenido)


# ---------------- CATEGORÍAS ----------------

@app.route("/categorias")
def listar_categorias():
    try:
        categorias = consultar("""
            SELECT idCategoria, nombreCategoria
            FROM categorias ORDER BY nombreCategoria
        """)

        filas = "".join(
            f"<tr><td>{c['idCategoria']}</td>"
            f"<td>{escape(c['nombreCategoria'])}</td></tr>"
            for c in categorias
        )

        contenido = """
        <a href="/categorias/nueva">+ Registrar categoría</a>
        <table><tr><th>ID</th><th>Nombre de categoría</th></tr>
        """ + filas + "</table>"

        return pagina("Gestión de categorías", contenido)
    except Exception as error:
        return f"Error al consultar categorías: {escape(error)}", 500


@app.route("/categorias/nueva", methods=["GET", "POST"])
def nueva_categoria():
    if request.method == "POST":
        nombre = request.form["nombreCategoria"].strip()
        if not nombre:
            return "El nombre de la categoría es obligatorio.", 400

        try:
            ejecutar(
                "INSERT INTO categorias (nombreCategoria) VALUES (%s)",
                (nombre,)
            )
            flash("Categoría registrada correctamente.")
            return redirect(url_for("listar_categorias"))
        except Exception as error:
            return f"Error al registrar categoría. Verifique que no exista ya: {escape(error)}", 400

    contenido = """
    <form method="POST">
        <label>Nombre de la categoría *</label>
        <input name="nombreCategoria" maxlength="80" required>
        <button type="submit">Guardar categoría</button>
    </form>
    """
    return pagina("Registrar categoría", contenido)


# ---------------- USUARIOS ----------------

@app.route("/usuarios")
def listar_usuarios():
    try:
        usuarios = consultar("""
            SELECT u.idUsuario, u.nombre, u.usuario, u.estado,
                   u.fechaRegistro, r.nombreRol
            FROM usuarios u
            INNER JOIN roles r ON u.idRol = r.idRol
            ORDER BY u.nombre
        """)

        filas = "".join(
            "<tr>" +
            "".join(f"<td>{escape(str(u.get(k) or ''))}</td>" for k in
                    ["idUsuario", "nombre", "usuario", "estado", "fechaRegistro", "nombreRol"]) +
            "</tr>"
            for u in usuarios
        )

        contenido = """
        <a href="/usuarios/nuevo">+ Registrar usuario</a>
        <table><tr><th>ID</th><th>Nombre</th><th>Usuario</th>
        <th>Estado</th><th>Fecha de registro</th><th>Rol</th></tr>
        """ + filas + "</table>"

        return pagina("Gestión de usuarios", contenido)
    except Exception as error:
        return f"Error al consultar usuarios: {escape(error)}", 500


@app.route("/usuarios/nuevo", methods=["GET", "POST"])
def nuevo_usuario():
    if request.method == "POST":
        try:
            nombre = request.form["nombre"].strip()
            usuario = request.form["usuario"].strip()
            contrasena = request.form["contrasena"]
            estado = request.form["estado"]
            id_rol = request.form["idRol"]

            if not nombre or not usuario or not contrasena:
                return "Complete los campos obligatorios.", 400

            contrasena_segura = generate_password_hash(contrasena)

            ejecutar("""
                INSERT INTO usuarios
                    (nombre, usuario, contrasena, estado, idRol)
                VALUES (%s, %s, %s, %s, %s)
            """, (nombre, usuario, contrasena_segura, estado, id_rol))

            flash("Usuario registrado correctamente.")
            return redirect(url_for("listar_usuarios"))
        except Exception as error:
            return f"Error al registrar usuario: {escape(error)}", 500

    try:
        roles = consultar("SELECT idRol, nombreRol FROM roles ORDER BY nombreRol")

        opciones = "".join(
            f'<option value="{r["idRol"]}">{escape(r["nombreRol"])}</option>'
            for r in roles
        )

        contenido = """
        <form method="POST">
            <label>Nombre completo *</label>
            <input name="nombre" maxlength="100" required>
            <label>Nombre de usuario *</label>
            <input name="usuario" maxlength="50" required>
            <label>Contraseña *</label>
            <input type="password" name="contrasena" required>
            <label>Estado</label>
            <select name="estado">
                <option value="Activo">Activo</option>
                <option value="Inactivo">Inactivo</option>
            </select>
            <label>Rol</label>
            <select name="idRol">""" + opciones + """</select>
            <button type="submit">Guardar usuario</button>
        </form>
        """
        return pagina("Registrar usuario", contenido)
    except Exception as error:
        return f"Error al consultar roles: {escape(error)}", 500



# ---------------- INVENTARIO ----------------

@app.route("/inventario")
def listar_inventario():
    try:
        productos = consultar("""
            SELECT
                p.idProducto,
                p.codigo,
                p.nombre,
                p.unidadMedida,
                COALESCE(i.existencia, 0) AS existencia,
                COALESCE(i.stockMinimo, p.stockMinimo, 0) AS stockMinimo,
                i.fechaActualizacion
            FROM productos p
            LEFT JOIN inventario i
                ON p.idProducto = i.idProducto
            ORDER BY p.nombre
        """)

        filas = ""

        for p in productos:
            existencia = float(p["existencia"] or 0)
            minimo = float(p["stockMinimo"] or 0)

            if existencia <= minimo:
                estado = (
                    '<span class="estado estado-inactivo">'
                    'Stock bajo</span>'
                )
            else:
                estado = (
                    '<span class="estado estado-activo">'
                    'Disponible</span>'
                )

            filas += f"""
                <tr>
                    <td>{escape(str(p['codigo']))}</td>
                    <td>{escape(str(p['nombre']))}</td>
                    <td>{existencia:.2f} {escape(str(p['unidadMedida']))}</td>
                    <td>{minimo:.2f}</td>
                    <td>{estado}</td>
                    <td>
                        <a href="/inventario/actualizar/{p['idProducto']}">
                            Actualizar
                        </a>
                    </td>
                </tr>
            """

        if not filas:
            filas = """
                <tr>
                    <td colspan="6">No hay productos registrados.</td>
                </tr>
            """

        contenido = f"""
            <p>
                <a href="/productos">Ver productos</a>
            </p>

            <div class="contenedor-tabla">
                <table>
                    <thead>
                        <tr>
                            <th>Código</th>
                            <th>Producto</th>
                            <th>Existencia</th>
                            <th>Stock mínimo</th>
                            <th>Estado</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas}
                    </tbody>
                </table>
            </div>
        """

        return pagina("Control de inventario", contenido)

    except Exception as error:
        return f"Error al consultar inventario: {escape(str(error))}", 500


@app.route(
    "/inventario/actualizar/<int:id_producto>",
    methods=["GET", "POST"]
)
def actualizar_inventario(id_producto):
    try:
        resultado = consultar("""
            SELECT
                p.idProducto,
                p.nombre,
                p.stockMinimo AS minimo_producto,
                i.existencia,
                i.stockMinimo AS minimo_inventario
            FROM productos p
            LEFT JOIN inventario i
                ON p.idProducto = i.idProducto
            WHERE p.idProducto = %s
        """, (id_producto,))

        if not resultado:
            flash("El producto no existe.")
            return redirect(url_for("listar_inventario"))

        producto = resultado[0]

        if request.method == "POST":
            try:
                existencia = float(request.form["existencia"])
                stock_minimo = float(request.form["stockMinimo"])

                if existencia < 0 or stock_minimo < 0:
                    flash("Las cantidades no pueden ser negativas.")
                    return redirect(
                        url_for(
                            "actualizar_inventario",
                            id_producto=id_producto
                        )
                    )

                ejecutar("""
                    INSERT INTO inventario
                        (idProducto, existencia, stockMinimo)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        existencia = VALUES(existencia),
                        stockMinimo = VALUES(stockMinimo),
                        fechaActualizacion = CURRENT_TIMESTAMP
                """, (id_producto, existencia, stock_minimo))

                flash("Inventario actualizado correctamente.")
                return redirect(url_for("listar_inventario"))

            except (ValueError, KeyError):
                flash("Ingrese cantidades numéricas válidas.")
                return redirect(
                    url_for(
                        "actualizar_inventario",
                        id_producto=id_producto
                    )
                )

        existencia = producto["existencia"]
        minimo = producto["minimo_inventario"]

        if existencia is None:
            existencia = 0

        if minimo is None:
            minimo = producto["minimo_producto"] or 0

        contenido = f"""
            <div class="panel">
                <h3>{escape(str(producto['nombre']))}</h3>

                <form method="POST">
                    <label for="existencia">Existencia actual</label>
                    <input
                        type="number"
                        id="existencia"
                        name="existencia"
                        min="0"
                        step="0.01"
                        value="{existencia}"
                        required
                    >

                    <label for="stockMinimo">Stock mínimo</label>
                    <input
                        type="number"
                        id="stockMinimo"
                        name="stockMinimo"
                        min="0"
                        step="0.01"
                        value="{minimo}"
                        required
                    >

                    <button type="submit">Guardar cambios</button>
                    <a href="/inventario">Volver al inventario</a>
                </form>
            </div>
        """

        return pagina("Actualizar inventario", contenido)

    except Exception as error:
        return f"Error al actualizar inventario: {escape(str(error))}", 500

if __name__ == "__main__":
    app.run(debug=True)

