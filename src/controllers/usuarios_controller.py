
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash

from src.utils.db import consultar, ejecutar


usuarios_bp = Blueprint('usuarios', __name__)


@usuarios_bp.route('/usuarios')
def listar_usuarios():

    usuarios = consultar("""
        SELECT
            u.idUsuario,
            u.nombre,
            u.usuario,
            u.estado,
            u.fechaRegistro,
            r.nombreRol AS rol
        FROM usuarios u
        INNER JOIN roles r
            ON u.idRol = r.idRol
        ORDER BY u.idUsuario DESC
    """)

    return render_template(
        'usuarios/lista.html',
        usuarios=usuarios
    )


@usuarios_bp.route('/usuarios/nuevo', methods=['GET', 'POST'])
def nuevo_usuario():

    if request.method == 'POST':

        nombre = request.form.get('nombre', '').strip()
        usuario = request.form.get('usuario', '').strip()
        contrasena = request.form.get('contrasena', '')
        estado = request.form.get('estado', 'Activo')
        id_rol = request.form.get('idRol')

        if not nombre or not usuario or not contrasena or not id_rol:
            flash('Todos los campos son obligatorios.', 'error')

        else:
            contrasena_hash = generate_password_hash(contrasena)

            try:
                ejecutar("""
                    INSERT INTO usuarios
                    (nombre, usuario, contrasena, estado, idRol)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    nombre,
                    usuario,
                    contrasena_hash,
                    estado,
                    id_rol
                ))

                flash('Usuario registrado correctamente.', 'success')
                return redirect(url_for('usuarios.listar_usuarios'))

            except Exception as error:
                flash(f'Error al registrar el usuario: {error}', 'error')

    roles = consultar("""
        SELECT idRol, nombreRol
        FROM roles
        ORDER BY nombreRol
    """)

    return render_template(
        'usuarios/nuevo.html',
        roles=roles
    )
