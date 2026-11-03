from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.utils.db import consultar, ejecutar


clientes_bp = Blueprint('clientes', __name__)


@clientes_bp.route('/clientes')
def listar_clientes():
    clientes = consultar("""
        SELECT idCliente, documento, nombre, telefono, direccion, correo
        FROM clientes
        ORDER BY nombre
    """)

    return render_template(
        'clientes/lista.html',
        clientes=clientes
    )


@clientes_bp.route('/clientes/nuevo', methods=['GET', 'POST'])
def nuevo_cliente():

    if request.method == 'POST':
        documento = request.form.get('documento', '').strip()
        nombre = request.form.get('nombre', '').strip()
        telefono = request.form.get('telefono', '').strip() or None
        direccion = request.form.get('direccion', '').strip() or None
        correo = request.form.get('correo', '').strip() or None

        if not documento or not nombre:
            flash('El documento y el nombre son obligatorios.', 'error')
            return redirect(url_for('clientes.nuevo_cliente'))

        try:
            ejecutar("""
                INSERT INTO clientes
                (documento, nombre, telefono, direccion, correo)
                VALUES (%s, %s, %s, %s, %s)
            """, (documento, nombre, telefono, direccion, correo))

            flash('Cliente registrado correctamente.', 'success')
            return redirect(url_for('clientes.listar_clientes'))

        except Exception as error:
            flash(f'Error al registrar el cliente: {error}', 'error')

    return render_template('clientes/nuevo.html')