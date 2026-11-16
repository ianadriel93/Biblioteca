# Sistema de Biblioteca

Aplicación de escritorio para gestionar una biblioteca/librería: libros, clientes y compras.
Hecha en **Python** con **CustomTkinter** (interfaz) y **SQLite** (base de datos).

Proyecto de estudio de la Tecnicatura Superior en Desarrollo de Software (ISPC).

## Funciones

- **Libros**: agregar, modificar, eliminar y listar (título, autor, precio, stock).
- **Clientes**: agregar, modificar, eliminar y listar (nombre y DNI, sin repetir DNI).
- **Compras**: registrar la compra de un libro por un cliente, ver el historial y anularla.
  - Al registrar una compra se descuenta el stock; al anularla, se devuelve.
  - Si no hay stock suficiente, la compra no se registra.
  - No se puede eliminar un libro o cliente que ya tiene compras.

## Requisitos

- Python 3.10 o superior
- Librería `customtkinter` (ver `requirements.txt`)

## Cómo ejecutarlo

Desde la carpeta del proyecto:

```
python -m pip install -r requirements.txt
python main.py
```

En Windows también funciona con `py -m pip install -r requirements.txt` y `py main.py`.

La primera vez se crea solo el archivo `datos/biblioteca.db`.

## Estructura del proyecto

```
BIBLIOTECA/
├── main.py                  → arranca la aplicación
├── probar.py                → script de prueba de la capa de datos
├── requirements.txt         → dependencias
├── datos/
│   └── biblioteca.db        → base de datos (se crea sola)
├── base_datos/              → capa de datos (SQL)
│   ├── conexion.py          → abre la base y activa las claves foráneas
│   ├── libros_db.py
│   ├── clientes_db.py
│   └── compras_db.py
└── interfaz/                → capa de interfaz (pantallas)
    ├── ventana_principal.py → ventana y pestañas
    ├── libros.py
    ├── clientes.py
    └── compras.py
```

## Arquitectura

El proyecto está separado en tres capas:

1. **Interfaz** (`interfaz/`): ventanas, formularios y tablas. Valida lo que escribe el usuario. No contiene SQL.
2. **Capa de datos** (`base_datos/`): funciones CRUD con las consultas SQL. No contiene widgets.
3. **Base de datos** (`datos/biblioteca.db`): archivo SQLite.

## Conceptos aplicados

- **CRUD**: crear, leer, modificar y eliminar registros.
- **Consultas parametrizadas** (`?`) para evitar la inyección SQL.
- **Restricciones SQL**: `NOT NULL`, `CHECK`, `UNIQUE`, `PRIMARY KEY AUTOINCREMENT`.
- **Claves foráneas** (`FOREIGN KEY` + `PRAGMA foreign_keys = ON`).
- **Manejo de errores** con `try / except / finally`, convirtiendo `sqlite3.IntegrityError` en `ValueError` con mensajes claros.
- **Transacciones** (`BEGIN IMMEDIATE`, `commit`, `rollback`) al registrar y anular compras.
- **JOIN** para mostrar el historial de compras con el nombre del cliente y el título del libro.
- **Eventos** en la interfaz: `command=` en botones y `bind("<<TreeviewSelect>>")` en las tablas.
- **Validación de datos** del formulario (campos vacíos, números, valores negativos, DNI).

## Probar la capa de datos

`probar.py` ejecuta pruebas sobre las funciones de `base_datos` sin abrir la interfaz. Se ejecuta desde la carpeta raíz:

```
python probar.py
```

> Importante: los archivos de `base_datos/` e `interfaz/` no se ejecutan directamente. Siempre se arranca desde la raíz con `main.py` o `probar.py`.

## Autor

Ian Montoya — Tecnicatura Superior en Desarrollo de Software, ISPC.
