import os
from peewee import MySQLDatabase

# Configuración de la base de datos
DATABASE = MySQLDatabase(
    'almacen_db',
    user='root',
    password='[Klisten1a3218]',
    host='localhost',
    port=3306
)

# Configuración de Flask
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-predeterminada')
DEBUG = True
