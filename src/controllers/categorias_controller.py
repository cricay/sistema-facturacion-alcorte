
from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.utils.db import consultar, ejecutar


categorias_bp = Blueprint('categorias', __name__)


@categorias_bp.route('/categorias')
def listar_categorias():

    categorias = consultar("""
        SELECT
            idCategoria,
            nombreCategoria
        FROM categorias
        ORDER BY nombreCategoria
    """)

    return render_template(
        'categorias/lista.html',
        categorias=categorias
    )


@categorias_bp.route('/categorias/nueva', methods=['GET', 'POST'])
def nueva_categoria():

    if request.method == 'POST':

        nombre_categoria = request.form.get('nombreCategoria', '').strip()

        if not nombre_categoria:
            flash('El nombre de la categoría es obligatorio.', 'error')
        else:
            try:
                ejecutar("""
                    INSERT INTO categorias (nombreCategoria)
                    VALUES (%s)
                """, (nombre_categoria,))

                flash('Categoría registrada correctamente.', 'success')
                return redirect(url_for('categorias.listar_categorias'))

            except Exception as error:
                flash(f'Error al registrar la categoría: {error}', 'error')

    return render_template('categorias/nueva.html')
