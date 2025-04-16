from datetime import datetime, timedelta
from models.venta import Venta
from models.detalle_venta import DetalleVenta
from models.producto import Producto
from peewee import fn, SQL

def get_ventas_periodo(periodo='diario'):
    """
    Obtiene las ventas según el periodo especificado
    """
    today = datetime.now()
    
    if periodo == 'diario':
        # Ventas del día
        start_date = datetime(today.year, today.month, today.day, 0, 0, 0)
        end_date = datetime(today.year, today.month, today.day, 23, 59, 59)
    elif periodo == 'semanal':
        # Ventas de la semana (desde el lunes)
        day_of_week = today.weekday()
        start_date = today - timedelta(days=day_of_week)
        start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
        end_date = datetime(today.year, today.month, today.day, 23, 59, 59)
    elif periodo == 'mensual':
        # Ventas del mes
        start_date = datetime(today.year, today.month, 1, 0, 0, 0)
        end_date = datetime(today.year, today.month, today.day, 23, 59, 59)
    else:
        # Período personalizado (usar fechas exactas)
        if isinstance(periodo, tuple) and len(periodo) == 2:
            start_date, end_date = periodo
        else:
            raise ValueError("Formato de periodo no válido")
    
    ventas = Venta.select().where(
        (Venta.fecha >= start_date) & 
        (Venta.fecha <= end_date)
    ).order_by(Venta.fecha.desc())
    
    return ventas, start_date, end_date

def get_productos_mas_vendidos(start_date, end_date, limit=10):
    """
    Obtiene los productos más vendidos en un periodo
    """
    return (DetalleVenta
        .select(
            DetalleVenta.producto,
            fn.SUM(DetalleVenta.cantidad).alias('total_vendido'),
            fn.SUM(DetalleVenta.subtotal).alias('total_ingresos')
        )
        .join(Venta)
        .where(
            (Venta.fecha >= start_date) & 
            (Venta.fecha <= end_date)
        )
        .group_by(DetalleVenta.producto)
        .order_by(SQL('total_vendido').desc())
        .limit(limit)
    )

def get_ventas_por_categoria(start_date, end_date):
    """
    Obtiene las ventas agrupadas por categoría de producto
    """
    return (DetalleVenta
        .select(
            Producto.categoria,
            fn.SUM(DetalleVenta.cantidad).alias('cantidad'),
            fn.SUM(DetalleVenta.subtotal).alias('total')
        )
        .join(Venta)
        .switch(DetalleVenta)
        .join(Producto)
        .where(
            (Venta.fecha >= start_date) & 
            (Venta.fecha <= end_date)
        )
        .group_by(Producto.categoria)
        .order_by(SQL('total').desc())
    )

def get_ventas_por_dia(start_date, end_date):
    """
    Obtiene las ventas agrupadas por día
    """
    ventas = Venta.select().where(
        (Venta.fecha >= start_date) & 
        (Venta.fecha <= end_date)
    )
    
    ventas_por_dia = {}
    for venta in ventas:
        fecha = venta.fecha.strftime('%Y-%m-%d')
        if fecha not in ventas_por_dia:
            ventas_por_dia[fecha] = {
                'fecha': fecha,
                'cantidad': 0,
                'total': 0
            }
        
        ventas_por_dia[fecha]['cantidad'] += 1
        ventas_por_dia[fecha]['total'] += float(venta.total)
    
    return sorted(ventas_por_dia.values(), key=lambda x: x['fecha'])

def get_rendimiento_productos(start_date, end_date):
    """
    Calcula el rendimiento de productos (rotación, margen, etc.)
    """
    # Aquí podrías implementar cálculos más avanzados de rendimiento
    # como rotación de inventario, margen bruto, etc.
    # Este es un ejemplo básico
    ventas_productos = get_productos_mas_vendidos(start_date, end_date, limit=None)
    
    rendimiento = []
    for producto_venta in ventas_productos:
        producto = producto_venta.producto
        cantidad = producto_venta.total_vendido
        ingresos = producto_venta.total_ingresos
        
        # Calcular rotación (ventas/stock actual)
        rotacion = 0
        if producto.stock > 0:
            rotacion = cantidad / producto.stock
        
        rendimiento.append({
            'producto': producto,
            'cantidad_vendida': cantidad,
            'ingresos': ingresos,
            'rotacion': rotacion
        })
    
    return rendimiento

def generar_resumen_informe(periodo, fecha_inicio=None, fecha_fin=None):
    """
    Genera un resumen completo para el informe
    """
    if fecha_inicio and fecha_fin:
        # Usar fechas personalizadas
        start_date = datetime.strptime(fecha_inicio, '%Y-%m-%d') if isinstance(fecha_inicio, str) else fecha_inicio
        end_date = datetime.strptime(fecha_fin, '%Y-%m-%d') if isinstance(fecha_fin, str) else fecha_fin
        ventas, _, _ = get_ventas_periodo((start_date, end_date))
    else:
        # Usar periodo predefinido
        ventas, start_date, end_date = get_ventas_periodo(periodo)
    
    # Calcular totales
    total_ventas = sum(venta.total for venta in ventas)
    cantidad_ventas = len(ventas)
    
    # Obtener productos más vendidos
    productos_vendidos = get_productos_mas_vendidos(start_date, end_date)
    
    # Obtener ventas por categoría
    ventas_por_categoria = get_ventas_por_categoria(start_date, end_date)
    
    # Obtener ventas por día
    ventas_por_dia = get_ventas_por_dia(start_date, end_date)
    
    return {
        'periodo': periodo,
        'fecha_inicio': start_date,
        'fecha_fin': end_date,
        'total_ventas': total_ventas,
        'cantidad_ventas': cantidad_ventas,
        'productos_vendidos': productos_vendidos,
        'ventas_por_categoria': ventas_por_categoria,
        'ventas_por_dia': ventas_por_dia,
        'ventas': ventas
    }
