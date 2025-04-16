from peewee import *
from datetime import datetime
from models.base_model import BaseModel

class Producto(BaseModel):
    codigo = CharField(max_length=20, unique=True)
    nombre = CharField(max_length=100)
    descripcion = TextField(null=True)
    precio = DecimalField(decimal_places=2)
    stock = IntegerField(default=0)
    categoria = CharField(max_length=50)
    fecha_creacion = DateTimeField(default=datetime.now)
    ultima_actualizacion = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'productos'
