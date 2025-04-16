from models.venta import Venta
from models.detalle_venta import DetalleVenta
from models.producto import Producto
from datetime import datetime
import peewee

def get_all_ventas():
    return Venta.select().order_by(Venta.fecha.desc())

def get_venta_by_id(id):
    try:
        return Venta.get_by_id(id)
    except Venta.DoesNotExist:
        return None

def create_venta(data):
    try:
        # Iniciar una transacción
        with peewee.database.atomic():
            # Crear la venta
            venta = Venta.create(
                fecha=datetime.now(),
                cliente=data.get('cliente', None),
                metodo_pago=data['metodo_pago'],
                total=data['total'],
                notas=data.get('notas', None)
            )
            
            # Agregar los detalles y actualizar stock
            for detalle in data['detalles']:
                producto = Producto.get_by_id(detalle['producto_id'])
                
                # Verificar stock
                if producto.stock < detalle['cantidad']:
                    raise Exception(f"Stock insuficiente para {producto.nombre}")
                
                # Crear detalle
                DetalleVenta.create(
                    venta=venta,
                    producto=producto,
                    cantidad=detalle['cantidad'],
                    precio_unitario=detalle['precio_unitario'],
                    subtotal=detalle['subtotal']
                )
                
                # Actualizar stock
                producto.stock -= detalle['cantidad']
                producto.save()
            
            return True, venta
    except Exception as e:
        return False, str(e)

def get_ventas_by_date_range(fecha_inicio, fecha_fin):
    return Venta.select().where(
        (Venta.fecha >= fecha_inicio) & 
        (Venta.fecha <= fecha_fin)
    ).order_by(Venta.fecha.desc())
