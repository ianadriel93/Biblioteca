from base_datos.libros_db import crear_tabla_libros, agregar_libro, obtener_libros

crear_tabla_libros()
agregar_libro("Rayuela", "Cortázar", 100, 5)
print(obtener_libros())