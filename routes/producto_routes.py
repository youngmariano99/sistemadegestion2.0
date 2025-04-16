from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from controllers.producto_controller import *

producto_bp = Blueprint('productos', __name__)

@producto_bp.route('/')
def lista_productos():
    productos = get_all_productos()
    return render_template('productos/lista.html', productos=productos)

@producto_bp.route('/crear', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        data = {
            'codigo': request.form['codigo'],
            'nombre': request.form['nombre'],
            'descripcion': request.form['descripcion'],
            'precio': float(request.form['precio']),
            'stock': int(request.form['stock']),
            'categoria': request.form['categoria']
        }
        
        success, result = create_producto(data)
        
        if success:
            flash('Producto creado correctamente', 'success')
            return redirect(url_for('productos.lista_productos'))
        else:
            flash(f'Error: {result}', 'error')
    
    return render_template('productos/crear.html')

@producto_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = get_producto_by_id(id)
    
    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('productos.lista_productos'))
    
    if request.method == 'POST':
        data = {
            'codigo': request.form['codigo'],
            'nombre': request.form['nombre'],
            'descripcion': request.form['descripcion'],
            'precio': float(request.form['precio']),
            'stock': int(request.form['stock']),
            'categoria': request.form['categoria']
        }
        
        success, result = update_producto(id, data)
        
        if success:
            flash('Producto actualizado correctamente', 'success')
            return redirect(url_for('productos.lista_productos'))
        else:
            flash(f'Error: {result}', 'error')
    
    return render_template('productos/editar.html', producto=producto)

@producto_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    success, result = delete_producto(id)
    
    if success:
        flash('Producto eliminado correctamente', 'success')
    else:
        flash(f'Error: {result}', 'error')
    
    return redirect(url_for('productos.lista_productos'))

# API para obtener producto (útil para AJAX)
@producto_bp.route('/api/<int:id>')
def api_get_producto(id):
    producto = get_producto_by_id(id)
    if producto:
        return jsonify({
            'id': producto.id,
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'stock': producto.stock
        })
    return jsonify({'error': 'Producto no encontrado'}), 404
