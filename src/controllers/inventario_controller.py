from flask import Blueprint, render_template

from src.utils.db import consultar


inventario_bp = Blueprint('inventario', __name__)


@inventario_bp.route('/inventario')
def listar_inventario():

    inventario = consultar("""
        SELECT
            i.idInventario,
            i.idProducto,
            p.nombre,
            i.existencia,
            i.stockMinimo,
            i.fechaActualizacion
        FROM inventario i
        INNER JOIN productos p
            ON i.idProducto = p.idProducto
        ORDER BY p.nombre
    """)

    return render_template(
        'inventario/lista.html',
        inventario=inventario
    )