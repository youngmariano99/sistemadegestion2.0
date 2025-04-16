from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from controllers.venta_controller import *
from datetime import datetime

venta_bp = Blueprint('ventas', __name__)

@venta_bp.route('/')
def lista_ventas():
    ventas = get_all_ventas()
    return render_template('ventas/lista.html', ventas=ventas)

@venta_bp.route('/crear', methods=['GET', 'POST'])
def crear_venta():
    if request.method == 'POST':
        try:
            # Procesar datos del formulario
            detalles = []
            for i in range(len(request.form.getlist('producto_id[]'))):
                detalles.append({
                    'producto_id': int(request.form.getlist('producto_id[]')[i]),
                    'cantidad': int(request.form.getlist('cantidad[]')[i]),
                    'precio_unitario': float(request.form.getlist('precio_unitario[]')[i]),
                    'subtotal': float(request.form.getlist('subtotal[]')[i])
                })
            
            data = {
                'cliente': request.form.get('cliente'),
                'metodo_pago': request.form['metodo_pago'],
                'total': float(request.form['total']),
                'notas': request.form.get('notas'),
                'detalles': detalles
            }
            
            success, result = create_venta(data)
            
            if success:
                flash('Venta registrada correctamente', 'success')
                return redirect(url_for('ventas.lista_ventas'))
            else:
                flash(f'Error: {result}', 'error')
        
        except Exception as e:
            flash(f'Error en el formulario: {str(e)}', 'error')
    
    # Obtener lista de productos para el formulario
    from controllers.producto_controller import get_all_productos
    productos = get_all_productos()
    return render_template('ventas/crear.html', productos=productos)

@venta_bp.route('/detalle/<int:id>')
def detalle_venta(id):
    venta = get_venta_by_id(id)
    if not venta:
        flash('Venta no encontrada', 'error')
        return redirect(url_for('ventas.lista_ventas'))
    
    # Los detalles son accesibles a través del backref definido en el modelo
    return render_template('ventas/detalle.html', venta=venta)
