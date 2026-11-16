from contextlib import closing

from base_datos.clientes_db import crear_tabla_clientes
from base_datos.conexion import obtener_conexion
from base_datos.libros_db import crear_tabla_libros


def crear_tabla_compras():
    crear_tabla_clientes()
    crear_tabla_libros()

    with closing(obtener_conexion()) as conexion:
        conexion.execute(
          """CREATE TABLE IF NOT EXISTS compras(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          cliente_id INTEGER NOT NULL,
          libro_id INTEGER NOT NULL,
          cantidad INTEGER NOT NULL CHECK (cantidad > 0),
          precio_unitario REAL NOT NULL,
          total REAL NOT NULL,
          fecha TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
          FOREIGN KEY (cliente_id) REFERENCES clientes(id),
          FOREIGN KEY (libro_id) REFERENCES libros(id)
          )    
          """
        )
        conexion.commit()


def obtener_compras():
    with closing(obtener_conexion()) as conexion:
        cursor = conexion.execute(
           """
           SELECT c.id, c.fecha, cl.nombre, l.titulo, c.cantidad, c.total
           FROM compras AS c
           JOIN clientes AS cl ON cl.id = c.cliente_id
           JOIN libros AS l ON l.id = c.libro_id
           ORDER BY c.id DESC
           """
        )
        return cursor.fetchall()


def registrar_compra(cliente_id, libro_id, cantidad):
    conexion = obtener_conexion()
    try:
        conexion.execute("BEGIN IMMEDIATE")

        libro = conexion.execute(
            "SELECT titulo, precio, stock FROM libros WHERE id = ?", (libro_id,)
        ).fetchone()
        if libro is None:
            raise ValueError("El libro seleccionado ya no existe.")

        titulo, precio, stock = libro
        if cantidad > stock:
            raise ValueError(f"Stock insuficiente para '{titulo}'. Disponible: {stock}.")

        total = precio * cantidad
        conexion.execute(
            """
            INSERT INTO compras (cliente_id, libro_id, cantidad, precio_unitario, total)
            VALUES (?, ?, ?, ?, ?)
            """,
            (cliente_id, libro_id, cantidad, precio, total),
        )
        conexion.execute(
            "UPDATE libros SET stock = stock - ? WHERE id = ?", (cantidad, libro_id)
        )

        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()

def eliminar_compra(compra_id):
    conexion = obtener_conexion()
    try:
        conexion.execute("BEGIN IMMEDIATE")

        compra = conexion.execute(
            "SELECT libro_id, cantidad FROM compras WHERE id = ?", (compra_id,)
        ).fetchone()
        if compra is None:
            raise ValueError("La compra seleccionada ya no existe.")

        libro_id, cantidad = compra
        conexion.execute(
            "UPDATE libros SET stock = stock + ? WHERE id = ?", (cantidad, libro_id)
        )
        conexion.execute("DELETE FROM compras WHERE id = ?", (compra_id,))
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()



    