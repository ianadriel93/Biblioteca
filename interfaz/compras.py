import customtkinter as ctk
from tkinter import messagebox, ttk
from interfaz.libros import formatear_precio

from base_datos.clientes_db import obtener_clientes
from base_datos.compras_db import (
    crear_tabla_compras,
    eliminar_compra,
    obtener_compras,
    registrar_compra,
)
from base_datos.libros_db import obtener_libros


def crear_vista_compras(contenedor):
    crear_tabla_compras()

    contenedor.grid_columnconfigure(0, weight=1)
    contenedor.grid_rowconfigure(2, weight=1)

    # ---------- FORMULARIO ----------
    formulario = ctk.CTkFrame(contenedor)
    formulario.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    formulario.grid_columnconfigure((1, 3, 5), weight=1)

    ctk.CTkLabel(formulario, text="Cliente:").grid(row=0, column=0, padx=8, pady=8, sticky="e")
    combo_cliente = ctk.CTkComboBox(formulario, values=[], state="readonly")
    combo_cliente.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

    ctk.CTkLabel(formulario, text="Libro:").grid(row=0, column=2, padx=8, pady=8, sticky="e")
    combo_libro = ctk.CTkComboBox(formulario, values=[], state="readonly")
    combo_libro.grid(row=0, column=3, padx=8, pady=8, sticky="ew")

    ctk.CTkLabel(formulario, text="Cantidad:").grid(row=0, column=4, padx=8, pady=8, sticky="e")
    entrada_cantidad = ctk.CTkEntry(formulario, width=80)
    entrada_cantidad.grid(row=0, column=5, padx=8, pady=8, sticky="ew")

    # ---------- TABLA (historial) ----------
    columnas = ("id", "fecha", "cliente", "libro", "cantidad", "total")
    tabla = ttk.Treeview(contenedor, columns=columnas, show="headings")
    for columna, encabezado in zip(
        columnas, ("ID", "Fecha", "Cliente", "Libro", "Cantidad", "Total")
    ):
        tabla.heading(columna, text=encabezado)
        tabla.column(columna, width=120)
    tabla.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    # ---------- FUNCIONES ----------
    def sacar_id(texto):
        """De un texto como '3 - Don Quijote' devuelve el número 3."""
        return int(texto.split(" - ")[0])

    def actualizar():
        """Recarga las listas desplegables y el historial."""
        clientes = [f"{id_} - {nombre}" for id_, nombre, _dni in obtener_clientes()]
        libros = [
            f"{id_} - {titulo} (stock: {stock})"
            for id_, titulo, _autor, _precio, stock in obtener_libros()
        ]
        combo_cliente.configure(values=clientes)
        combo_libro.configure(values=libros)
        combo_cliente.set(clientes[0] if clientes else "")
        combo_libro.set(libros[0] if libros else "")

        for fila in tabla.get_children():
            tabla.delete(fila)
        for id_, fecha, cliente, libro, cantidad, total in obtener_compras():
            tabla.insert("", "end", values=(id_, fecha, cliente, libro, cantidad, formatear_precio(total)))

    def registrar():
        texto_cliente = combo_cliente.get()
        texto_libro = combo_libro.get()
        if not texto_cliente or not texto_libro:
            messagebox.showwarning("Atención", "Cargue al menos un cliente y un libro.")
            return

        try:
            cantidad = int(entrada_cantidad.get().strip())
        except ValueError:
            messagebox.showwarning("Atención", "La cantidad debe ser un número entero.")
            return
        if cantidad <= 0:
            messagebox.showwarning("Atención", "La cantidad debe ser mayor que cero.")
            return

        try:
            registrar_compra(sacar_id(texto_cliente), sacar_id(texto_libro), cantidad)
        except ValueError as error:
            messagebox.showerror("No se pudo registrar", str(error))
            return

        entrada_cantidad.delete(0, "end")
        actualizar()
        messagebox.showinfo("Compra", "Compra registrada correctamente.")

    def anular():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una compra de la tabla.")
            return
        if not messagebox.askyesno("Confirmar", "¿Anular la compra? El stock se devolverá."):
            return
        try:
            eliminar_compra(tabla.item(seleccion[0], "values")[0])
        except ValueError as error:
            messagebox.showerror("Error", str(error))
            return
        actualizar()

    # ---------- BOTONES ----------
    botones = ctk.CTkFrame(contenedor, fg_color="transparent")
    botones.grid(row=1, column=0, pady=5)
    ctk.CTkButton(botones, text="Registrar compra", command=registrar, width=140).pack(side="left", padx=5)
    ctk.CTkButton(botones, text="Anular compra", command=anular, width=140).pack(side="left", padx=5)

    actualizar()
    return actualizar