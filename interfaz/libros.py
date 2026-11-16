import customtkinter as ctk
from tkinter import messagebox, ttk

from base_datos.libros_db import (
    agregar_libro,
    crear_tabla_libros,
    eliminar_libro,
    modificar_libro,
    obtener_libros,
)


def formatear_precio(precio):
    """30000.0 -> '30.000'   |   30000.5 -> '30.000,50'"""
    texto = f"{precio:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    if texto.endswith(",00"):
        texto = texto[:-3]
    return texto


def texto_a_precio(texto):
    """'30.000' -> 30000.0   |   '30.000,50' -> 30000.5   |   '30000' -> 30000.0"""
    texto = texto.replace("$", "").replace(" ", "")
    if "," in texto:
        texto = texto.replace(".", "").replace(",", ".")
    else:
        texto = texto.replace(".", "")
    return float(texto)


def crear_vista_libros(contenedor):
    crear_tabla_libros()

    contenedor.grid_columnconfigure(0, weight=1)
    contenedor.grid_rowconfigure(2, weight=1)

    # ---------- FORMULARIO ----------
    formulario = ctk.CTkFrame(contenedor)
    formulario.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    formulario.grid_columnconfigure((1, 3), weight=1)

    entradas = {}
    campos = (("Título", 0, 0), ("Precio", 0, 2), ("Autor", 1, 0), ("Stock", 1, 2))
    for nombre, fila, columna in campos:
        ctk.CTkLabel(formulario, text=f"{nombre}:").grid(
            row=fila, column=columna, padx=8, pady=8, sticky="e"
        )
        entrada = ctk.CTkEntry(formulario)
        entrada.grid(row=fila, column=columna + 1, padx=8, pady=8, sticky="ew")
        entradas[nombre] = entrada

    # ---------- TABLA ----------
    columnas = ("id", "titulo", "autor", "precio", "stock")
    tabla = ttk.Treeview(contenedor, columns=columnas, show="headings")
    encabezados = ("ID", "Título", "Autor", "Precio", "Stock")
    anchos = (60, 320, 260, 140, 100)
    for columna, encabezado, ancho in zip(columnas, encabezados, anchos):
        tabla.heading(columna, text=encabezado)
        tabla.column(columna, width=ancho, minwidth=50, stretch=True, anchor="center")
    tabla.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    # ---------- FUNCIONES ----------
    def obtener_datos():
        titulo = entradas["Título"].get().strip()
        autor = entradas["Autor"].get().strip()
        texto_precio = entradas["Precio"].get().strip()
        texto_stock = entradas["Stock"].get().strip()

        if not titulo or not autor or not texto_precio or not texto_stock:
            messagebox.showwarning("Atención", "Complete todos los campos.")
            return None

        try:
            precio = texto_a_precio(texto_precio)
            stock = int(texto_stock)
        except ValueError:
            messagebox.showwarning("Atención", "Precio debe ser un número y stock entero.")
            return None

        if precio < 0 or stock < 0:
            messagebox.showwarning("Atención", "No se permiten valores negativos.")
            return None

        return titulo, autor, precio, stock

    def limpiar():
        for entrada in entradas.values():
            entrada.delete(0, "end")

    def actualizar():
        for fila in tabla.get_children():
            tabla.delete(fila)
        for id_libro, titulo, autor, precio, stock in obtener_libros():
            tabla.insert("", "end", values=(id_libro, titulo, autor, "$" + formatear_precio(precio), stock))

    def agregar():
        datos = obtener_datos()
        if datos:
            agregar_libro(*datos)
            limpiar()
            actualizar()

    def modificar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un libro de la tabla.")
            return
        datos = obtener_datos()
        if datos:
            id_libro = tabla.item(seleccion[0], "values")[0]
            modificar_libro(id_libro, *datos)
            limpiar()
            actualizar()

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un libro de la tabla.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el libro?"):
            return
        try:
            eliminar_libro(tabla.item(seleccion[0], "values")[0])
        except ValueError as error:
            messagebox.showerror("No se puede eliminar", str(error))
            return
        limpiar()
        actualizar()

    def cargar_seleccion(evento=None):
        seleccion = tabla.selection()
        if not seleccion:
            return
        valores = tabla.item(seleccion[0], "values")
        limpiar()
        entradas["Título"].insert(0, valores[1])
        entradas["Autor"].insert(0, valores[2])
        entradas["Precio"].insert(0, valores[3])
        entradas["Stock"].insert(0, valores[4])

    # ---------- BOTONES Y EVENTOS ----------
    botones = ctk.CTkFrame(contenedor, fg_color="transparent")
    botones.grid(row=1, column=0, pady=5)
    for texto, comando in (("Agregar", agregar), ("Modificar", modificar),
                           ("Eliminar", eliminar), ("Limpiar", limpiar)):
        ctk.CTkButton(botones, text=texto, command=comando, width=110).pack(side="left", padx=5)

    tabla.bind("<<TreeviewSelect>>", cargar_seleccion)

    actualizar()
    return actualizar