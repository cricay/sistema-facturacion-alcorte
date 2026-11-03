from flask import Flask


def create_app():

    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    app.secret_key = "alcorte_clave_local_2026"

    from src.controllers.home_controller import home_bp
    from src.controllers.productos_controller import productos_bp
    from src.controllers.clientes_controller import clientes_bp
    from src.controllers.categorias_controller import categorias_bp
    from src.controllers.usuarios_controller import usuarios_bp
    from src.controllers.inventario_controller import inventario_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(categorias_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(inventario_bp)

    return app