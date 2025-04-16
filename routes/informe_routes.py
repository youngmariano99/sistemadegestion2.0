from flask import Blueprint, render_template, request, jsonify, Response
from controllers.informe_controller import get_estadisticas_dashboard
from services.informe_service import generar_resumen_informe
from datetime import datetime, timedelta
import csv, io

informe_bp = Blueprint('informes', __name__)

@informe_bp.route('/')
def dashboard():
    # Obtener estadísticas para el dashboard
    estadisticas = get_estadisticas_dashboard()
    return render_template('informes/dashboard.html', estadisticas=estadisticas)

@informe_bp.route('/generar', methods=['GET', 'POST'])
def generar_informe():
    if request.method == 'POST':
        tipo_informe = request.form['tipo_informe']
        fecha_inicio = request.form['fecha_inicio']
        fecha_fin = request.form['fecha_fin']
        
        # Generar el informe según el tipo seleccionado
        informe = generar_resumen_informe(
            tipo_informe,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        
        # Si se solicita descargar como CSV
        if request.form.get('formato') == 'csv':
            return generar_csv(informe)
        
        return render_template(
            'informes/resultado.html', 
            informe=informe,
            tipo_informe=tipo_informe,
            fecha_inicio=informe['fecha_inicio'],
            fecha_fin=informe['fecha_fin']
        )
    
    # Configurar fechas predeterminadas (último mes)
    hoy = datetime.now()
    hace_un_mes = hoy - timedelta(days=30)
    
    return render_template(
        'informes/generar.html',
        fecha_inicio=hace_un_mes.strftime('%Y-%m-%d'),
        fecha_fin=hoy.strftime('%Y-%m-%d')
    )

def generar_csv(informe):
    # Crear buffer para el CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Escribir cabecera
    writer.writerow(['Informe de Ventas'])
    writer.writerow(['Periodo', informe['periodo']])
    writer.writerow(['Fecha Inicio', informe['fecha_inicio'].strftime('%d/%m/%Y')])
    writer.writerow(['Fecha Fin', informe['fecha_fin'].strftime('%d/%m/%Y')])
    writer.writerow(['Total Ventas', f"${informe['total_ventas']:.2f}"])
    writer.writerow(['Cantidad de Ventas', informe['cantidad_ventas']])
    writer.writerow([])
    
    # Productos vendidos
    writer.writerow(['Productos Más Vendidos'])
    writer.writerow(['Producto', 'Cantidad', 'Total'])
    
    for producto in informe['productos_vendidos']:
        writer.writerow([
            producto.producto.nombre,
            producto.total_vendido,
            f"${producto.total_ingresos:.2f}"
        ])
    
    writer.writerow([])
    
    # Ventas por categoría
    writer.writerow(['Ventas por Categoría'])
    writer.writerow(['Categoría', 'Cantidad', 'Total'])
    
    for categoria in informe['ventas_por_categoria']:
        writer.writerow([
            categoria.categoria,
            categoria.cantidad,
            f"${categoria.total:.2f}"
        ])
    
    # Preparar la respuesta
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=informe_{informe['periodo']}_{datetime.now().strftime('%Y%m%d')}.csv"}
    )
