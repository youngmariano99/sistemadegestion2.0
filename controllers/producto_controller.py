from models.producto import Producto
from datetime import datetime

def get_all_productos():
    return Producto.select().order_by(Producto.nombre)

def get_producto_by_id(id):
    try:
        return Producto.get_by_id(id)
    except Producto.DoesNotExist:
        return None

def get_producto_by_codigo(codigo):
    try:
        return Producto.get(Producto.codigo == codigo)
    except Producto.DoesNotExist:
        return None

def create_producto(data):
    try:
        # Verificar si ya existe un producto con el mismo código
        if get_producto_by_codigo(data['codigo']):
            return False, "Ya existe un producto con ese código"
        
        producto = Producto.create(
            codigo=data['codigo'],
            nombre=data['nombre'],
            descripcion=data.get('descripcion', ''),
            precio=data['precio'],
            stock=data['stock'],
            categoria=data['categoria'],
            fecha_creacion=datetime.now(),
            ultima_actualizacion=datetime.now()
        )
        return True, producto
    except Exception as e:
        return False, str(e)

def update_producto(id, data):
    try:
        producto = get_producto_by_id(id)
        if not producto:
            return False, "Producto no encontrado"
        
        # Si está actualizando el código, verificar que no exista
        if 'codigo' in data and data['codigo'] != producto.codigo:
            if get_producto_by_codigo(data['codigo']):
                return False, "Ya existe un producto con ese código"
        
        for key, value in data.items():
            setattr(producto, key, value)
        
        producto.ultima_actualizacion = datetime.now()
        producto.save()
        return True, producto
    except Exception as e:
        return False, str(e)

def delete_producto(id):
    try:
        producto = get_producto_by_id(id)
        if not producto:
            return False, "Producto no encontrado"
        producto.delete_instance()
        return True, "Producto eliminado correctamente"
    except Exception as e:
        return False, str(e)

def get_productos_stock_bajo(limite=5):
    return Producto.select().where(Producto.stock < limite)
