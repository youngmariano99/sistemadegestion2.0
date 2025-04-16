from models.producto import Producto
from models.venta import Venta
from models.detalle_venta import DetalleVenta
from peewee import fn, SQL
from datetime import datetime, timedelta

def get_estadisticas_dashboard():
    # Fecha de hoy y hace 30 días
    hoy = datetime.now()
    hace_30_dias = hoy - timedelta(days=30)
    
    # Total de productos
    total_productos = Producto.select().count()
    
    # Productos con stock bajo
    productos_stock_bajo = Producto.select().where(Producto.stock < 5).count()
    
    # Ventas del día
    ventas_hoy = Venta.select().where(
        fn.DATE(Venta.fecha) == hoy.date()
    ).count()
    
    # Total ventas del día
    total_ventas_hoy = Venta.select(fn.SUM(Venta.total).alias('suma')).where(
        fn.DATE(Venta.fecha) == hoy.date()
    ).scalar() or 0
    
    # Ventas últimos 30 días
    ventas_mes = Venta.select().where(
        Venta.fecha.between(hace_30_dias, hoy)
    ).count()
    
    # Total ventas últimos 30 días
    total_ventas_mes = Venta.select(fn.SUM(Venta.total).alias('suma')).where(
        Venta.fecha.between(hace_30_dias, hoy)
    ).scalar() or 0
    
    # Productos más vendidos (top 5)
    productos_top = (DetalleVenta
        .select(
            DetalleVenta.producto,
            fn.SUM(DetalleVenta.cantidad).alias('total_vendido')
        )
        .join(Venta)
        .where(Venta.fecha.between(hace_30_dias, hoy))
        .group_by(DetalleVenta.producto)
        .order_by(SQL('total_vendido').desc())
        .limit(5)
    )
    
    return {
        'total_productos': total_productos,
        'productos_stock_bajo': productos_stock_bajo,
        'ventas_hoy': ventas_hoy,
        'total_ventas_hoy': total_ventas_hoy,
        'ventas_mes': ventas_mes,
        'total_ventas_mes': total_ventas_mes,
        'productos_top': productos_top
    }

def generar_informe_ventas(tipo_informe, fecha_inicio, fecha_fin):
    # Obtener ventas en el rango de fechas
    ventas = Venta.select().where(
        Venta.fecha.between(fecha_inicio, fecha_fin)
    ).order_by(Venta.fecha)
    
    # Calcular total de ventas
    total = sum(venta.total for venta in ventas)
    
    # Agrupar ventas según el tipo de informe
    if tipo_informe == 'diario':
        # Agrupar por día
        ventas_agrupadas = {}
        for venta in ventas:
            fecha_str = venta.fecha.strftime('%Y-%m-%d')
            if fecha_str not in ventas_agrupadas:
                ventas_agrupadas[fecha_str] = {'total': 0, 'cantidad': 0}
            ventas_agrupadas[fecha_str]['total'] += venta.total
            ventas_agrupadas[fecha_str]['cantidad'] += 1
    
    elif tipo_informe == 'semanal':
        # Agrupar por semana
        ventas_agrupadas = {}
        for venta in ventas:
            # Obtener número de semana
            semana = venta.fecha.strftime('%Y-W%W')
            if semana not in ventas_agrupadas:
                ventas_agrupadas[semana] = {'total': 0, 'cantidad': 0}
            ventas_agrupadas[semana]['total'] += venta.total
            ventas_agrupadas[semana]['cantidad'] += 1
    
    else:  # mensual
        # Agrupar por mes
        ventas_agrupadas = {}
        for venta in ventas:
            mes = venta.fecha.strftime('%Y-%m')
            if mes not in ventas_agrupadas:
                ventas_agrupadas[mes] = {'total': 0, 'cantidad': 0}
            ventas_agrupadas[mes]['total'] += venta.total
            ventas_agrupadas[mes]['cantidad'] += 1
    
    # Obtener productos más vendidos
    productos_vendidos = (DetalleVenta
        .select(
            DetalleVenta.producto,
            fn.SUM(DetalleVenta.cantidad).alias('total_vendido'),
            fn.SUM(DetalleVenta.subtotal).alias('ingresos')
        )
        .join(Venta)
        .where(Venta.fecha.between(fecha_inicio, fecha_fin))
        .group_by(DetalleVenta.producto)
        .order_by(SQL('total_vendido').desc())
    )
    
    return {
        'ventas': ventas,
        'total': total,
        'ventas_agrupadas': ventas_agrupadas,
        'productos_vendidos': productos_vendidos
    }
