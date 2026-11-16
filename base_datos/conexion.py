"""Conexión con la base de datos SQLite.

Todas las funciones de datos llaman a ''obtener_conexion''. 
Así la ruta y la configuración están en un solo lugar 
y no se repiten en cada archivo.
"""

import sqlite3
from pathlib import Path

# __file__ es la ubicación  de este archivo.
# paren.parent subde dos niveles hasta la carpeta del proyecto.
#El operador / de Path une partes de la ruta en cualquier sistema operativo.
RUTA_BASE_DATOS = Path(__file__).resolve().parent.parent / "datos" / "biblioteca.db"

def obtener_conexion():
    """Abre y devuelve una conexión con la base de datos."""
    
    # Si la carpeta "datos" no existe, se crea.
    RUTA_BASE_DATOS.parent.mkdir(parents=True, exist_ok=True)

    # Si el archivo .db no existe, SQLite lo crea automáticamente.
    conexion = sqlite3.connect(RUTA_BASE_DATOS)

    # SQLite no controla las claves foráneas por defecto: hay que activarlas
    #en cada conexión nueva.
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion
