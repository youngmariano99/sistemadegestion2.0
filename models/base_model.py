from peewee import Model, DatabaseProxy

# Usamos un proxy de base de datos para inicializarlo más tarde
database_proxy = DatabaseProxy()

class BaseModel(Model):
    """Modelo base para todos los modelos de la aplicación"""
    class Meta:
        database = database_proxy
