"""CRUD de libros con SQL.
CRUD = Create  (crear), Read (leer), Update (actualizar), Delete (eliminar).
Este archivo NO tiene widgets: solo recibe datos y habla con SQLite.
"""

import sqlite3

from base_datos.conexion import obtener_conexion

def crear_tabla_libros():
    """Crea la tabla libros si todavía no existe."""
    
    conexion = obtener_conexion()
    try:
        # IF NOT EXISTS evita un error si la tabla ya fue creada"""
        # CHECK obliga a que precio y stock nunca sean negativos.
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            precio REAL NOT NULL CHECK (precio >= 0),
            stock INTEGER NOT NULL CHECK (stock >=0)
            )
            """
        )
        # commit guarda los cambios de forma permanente.
        conexion.commit()
    finally:
        # finally se ejecuta siempre, incluso si hubo un error.
        conexion.close()


def agregar_libro(titulo , autor , precio , stock):
    """CREATE: guarda un libro nuevo."""

    conexion = obtener_conexion()
    try:
        # Los ? son parámetros seguros. NUNCA se arma el SQL pegando texto,
        # porque eso permite la "inyección SQL".
        conexion.execute(
            "INSERT INTO libros (titulo , autor , precio , stock) VALUES (?, ?, ?, ?)",
            (titulo, autor, precio, stock),
        )
        conexion.commit()
    finally:
        conexion.close()


def obtener_libros():
    """READ: devuelve todos los libros como lista de tuplas."""

    conexion = obtener_conexion()
    try:
        cursor = conexion.execute(
            "SELECT id, titulo, autor, precio, stock FROM libros ORDER BY id"
        )
        #fetchall devuelve todas las filas del resultado.
        return cursor.fetchall()
    finally:
        conexion.close()


def modificar_libro(id_libro, titulo, autor, precio, stock):
    """UPDATE: cambia los datos del libro con ese id."""

    conexion = obtener_conexion()
    try:
        #WHERE id = ? hace que solo se modifique UNA fila.
        conexion.execute(
            "UPDATE libros SET titulo = ?, autor = ?, precio = ?,  stock = ? WHERE id = ?",
            (titulo, autor, precio, stock, id_libro),
        )
        conexion.commit()
    finally: 
        conexion.close()


def eliminar_libro(id_libro):
    """DELETE: borra el libro. Failla si el libro ya fue comprado."""


    conexion = obtener_conexion()
    try:
        conexion.execute("DELETE FROM libros WHERE id = ?" , (id_libro,))
        conexion.commit()
    except sqlite3.IntegrityError as error:
        #La clave foránea de "compras" impide borrar un libro que se usó.
        # Convertimos el error técnico en un mensaje claro para el usuario.
        raise ValueError("No se puede eliminar un libro que ya fue comprado") from error
    finally:
        conexion.close()
