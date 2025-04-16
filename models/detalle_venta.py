from peewee import *
from models.base_model import BaseModel
from .producto import Producto
from .venta import Venta

class DetalleVenta(BaseModel):
    venta = ForeignKeyField(Venta, backref='detalles')
    producto = ForeignKeyField(Producto, backref='ventas')
    cantidad = IntegerField()
    precio_unitario = DecimalField(decimal_places=2)
    subtotal = DecimalField(decimal_places=2)

    class Meta:
        table_name = 'detalles_venta'
