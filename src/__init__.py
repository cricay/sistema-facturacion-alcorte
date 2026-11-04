import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app():

    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    app.secret_key = os.getenv("SECRET_KEY")

    if not app.secret_key:
        raise RuntimeError("No se encontró SECRET_KEY en el archivo .env")

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