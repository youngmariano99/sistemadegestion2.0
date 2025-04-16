from peewee import *
from datetime import datetime
from models.base_model import BaseModel

class Venta(BaseModel):
    fecha = DateTimeField(default=datetime.now)
    cliente = CharField(max_length=100, null=True)
    metodo_pago = CharField(max_length=50)
    total = DecimalField(decimal_places=2)
    notas = TextField(null=True)

    class Meta:
        table_name = 'ventas'
