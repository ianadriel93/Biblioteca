import customtkinter as ctk
from tkinter import messagebox, ttk

from base_datos.clientes_db import (
    agregar_cliente,
    crear_tabla_clientes,
    eliminar_cliente,
    modificar_cliente,
    obtener_clientes,
)


def crear_vista_clientes(contenedor):
    crear_tabla_clientes()

    contenedor.grid_columnconfigure(0, weight=1)
    contenedor.grid_rowconfigure(2, weight=1)

    # ---------- FORMULARIO ----------
    formulario = ctk.CTkFrame(contenedor)
    formulario.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    formulario.grid_columnconfigure((1, 3), weight=1)

    entradas = {}
    for nombre, columna in (("Nombre", 0), ("DNI", 2)):
        ctk.CTkLabel(formulario, text=f"{nombre}:").grid(
            row=0, column=columna, padx=8, pady=8, sticky="e"
        )
        entrada = ctk.CTkEntry(formulario)
        entrada.grid(row=0, column=columna + 1, padx=8, pady=8, sticky="ew")
        entradas[nombre] = entrada

    # ---------- TABLA ----------
    columnas = ("id", "nombre", "dni")
    tabla = ttk.Treeview(contenedor, columns=columnas, show="headings")
    for columna, encabezado in zip(columnas, ("ID", "Nombre", "DNI")):
        tabla.heading(columna, text=encabezado)
        tabla.column(columna, width=150, anchor="center")
    tabla.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    # ---------- FUNCIONES ----------
    def obtener_datos():
        nombre = entradas["Nombre"].get().strip()
        dni = entradas["DNI"].get().strip()

        if not nombre or not dni:
            messagebox.showwarning("Atención", "Complete todos los campos.")
            return None
        # isdigit() es True solo si el texto tiene únicamente números.
        if not dni.isdigit():
            messagebox.showwarning("Atención", "El DNI debe tener solo números.")
            return None
        return nombre, dni

    def limpiar():
        for entrada in entradas.values():
            entrada.delete(0, "end")

    def actualizar():
        for fila in tabla.get_children():
            tabla.delete(fila)
        for fila in obtener_clientes():
            tabla.insert("", "end", values=fila)

    def agregar():
        datos = obtener_datos()
        if datos:
            try:
                agregar_cliente(*datos)
            except ValueError as error:
                messagebox.showerror("Error", str(error))
                return
            limpiar()
            actualizar()

    def modificar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un cliente de la tabla.")
            return
        datos = obtener_datos()
        if datos:
            id_cliente = tabla.item(seleccion[0], "values")[0]
            try:
                modificar_cliente(id_cliente, *datos)
            except ValueError as error:
                messagebox.showerror("Error", str(error))
                return
            limpiar()
            actualizar()

    def eliminar():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione un cliente de la tabla.")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar el cliente?"):
            return
        try:
            eliminar_cliente(tabla.item(seleccion[0], "values")[0])
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
        entradas["Nombre"].insert(0, valores[1])
        entradas["DNI"].insert(0, valores[2])

    # ---------- BOTONES Y EVENTOS ----------
    botones = ctk.CTkFrame(contenedor, fg_color="transparent")
    botones.grid(row=1, column=0, pady=5)
    for texto, comando in (("Agregar", agregar), ("Modificar", modificar),
                           ("Eliminar", eliminar), ("Limpiar", limpiar)):
        ctk.CTkButton(botones, text=texto, command=comando, width=110).pack(side="left", padx=5)

    tabla.bind("<<TreeviewSelect>>", cargar_seleccion)

    actualizar()
    return actualizar