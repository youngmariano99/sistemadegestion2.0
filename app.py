from flask import Flask, render_template, redirect, url_for
from config import DATABASE, SECRET_KEY, DEBUG
from models.base_model import database_proxy
from models.producto import Producto
from models.venta import Venta
from models.detalle_venta import DetalleVenta
from routes.producto_routes import producto_bp
from routes.venta_routes import venta_bp
from routes.informe_routes import informe_bp
from controllers.informe_controller import get_estadisticas_dashboard

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG

# Configuración de la base de datos
database_proxy.initialize(DATABASE)

# Crear tablas si no existen
def create_tables():
    with DATABASE:
        DATABASE.create_tables([Producto, Venta, DetalleVenta])

# Registro de blueprints
app.register_blueprint(producto_bp, url_prefix='/productos')
app.register_blueprint(venta_bp, url_prefix='/ventas')
app.register_blueprint(informe_bp, url_prefix='/informes')

@app.route('/')
def index():
    estadisticas = get_estadisticas_dashboard()
    return render_template('index.html', estadisticas=estadisticas)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    create_tables()
    app.run(host='0.0.0.0', port=5000)



