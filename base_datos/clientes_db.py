"""CRUD de clientes con SQL.

Igual que libros_db.py, pero la tabla tiene unu DNI único (UNIQUE).
"""

import sqlite3

from base_datos.conexion import obtener_conexion


def crear_tabla_clientes():
    """Crea la tabla clientes si todavía no existe."""

    conexion = obtener_conexion()
    try:
        # UNIQUE impide que dos clientes tengan el mismo DNI.
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                dni TEXT NOT NULL UNIQUE
            )
            """
        )
        conexion.commit()
    finally:
        conexion.close()


def agregar_cliente(nombre , dni):
    """CREATE: guarda un cliente nuevo."""

    conexion = obtener_conexion()
    try:
        conexion.execute(
            "INSERT INTO clientes (nombre, dni) VALUES (?, ?)", (nombre,dni)
        )
        conexion.commit()
    except sqlite3.IntegrityError as error:
        # Se rompió la restricción UNIQUE: ese DNI ya existe.
        raise ValueError("Ya existe un cliente con ese DNI.") from error
    finally:
        conexion.close()


def obtener_clientes():
    """READ: devuelve todos los clientes"""

    conexion = obtener_conexion()
    try:
        cursor = conexion.execute("SELECT id, nombre, dni FROM clientes ORDER BY id")
        return cursor.fetchall()
    finally:
        conexion.close()


def modificar_cliente(id_cliente, nombre, dni):
    """UPDATE: cambia los datos del cliente."""

    conexion = obtener_conexion()
    try:
        conexion.execute(
            "UPDATE clientes SET nombre = ?, dni = ? WHERE id = ?",
            (nombre, dni, id_cliente),
        )
        conexion.commit()
    except sqlite3.IntegrityError as error:
        raise ValueError("Ya existe un cliente con ese DNI.") from error
    finally:
        conexion.close()


def eliminar_cliente(id_cliente):
    """DELETE: borra el cliente. Falla si tiene compras."""

    conexion = obtener_conexion()
    try:
        conexion.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
        conexion.commit()
    except sqlite3.IntegrityError as error:
        raise ValueError("No se puede eliminar un cliente porque tiene compras.") from error
    finally:
        conexion.close()
