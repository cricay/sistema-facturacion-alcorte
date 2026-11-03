
from flask import Blueprint, render_template, request, redirect, url_for, flash

from src.utils.db import consultar, ejecutar


productos_bp = Blueprint('productos', __name__)


@productos_bp.route('/productos')
def listar_productos():

    productos = consultar("""
        SELECT
            p.idProducto,
            p.codigo,
            p.nombre,
            p.precio,
            p.unidadMedida,
            p.stockMinimo,
            p.estado,
            c.nombreCategoria AS categoria
        FROM productos p
        LEFT JOIN categorias c
            ON p.idCategoria = c.idCategoria
        ORDER BY p.idProducto DESC
    """)

    return render_template(
        'productos/lista.html',
        productos=productos
    )


@productos_bp.route('/productos/nuevo', methods=['GET', 'POST'])
def nuevo_producto():

    if request.method == 'POST':

        codigo = request.form.get('codigo', '').strip()
        nombre = request.form.get('nombre', '').strip()
        precio = request.form.get('precio')
        unidad_medida = request.form.get('unidadMedida')
        stock_minimo = request.form.get('stockMinimo')
        estado = request.form.get('estado')
        id_categoria = request.form.get('idCategoria')

        if not codigo or not nombre or not precio or not id_categoria:
            flash('Completa los campos obligatorios.', 'error')
        else:
            try:
                ejecutar("""
                    INSERT INTO productos
                    (codigo, nombre, precio, unidadMedida,
                     stockMinimo, estado, idCategoria)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    codigo,
                    nombre,
                    precio,
                    unidad_medida,
                    stock_minimo,
                    estado,
                    id_categoria
                ))

                flash('Producto registrado correctamente.', 'success')
                return redirect(url_for('productos.listar_productos'))

            except Exception as error:
                flash(f'Error al registrar el producto: {error}', 'error')

    categorias = consultar("""
        SELECT idCategoria, nombreCategoria
        FROM categorias
        ORDER BY nombreCategoria
    """)

    return render_template(
        'productos/nuevo.html',
        categorias=categorias
    )
