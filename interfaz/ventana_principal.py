import customtkinter as ctk

from interfaz.clientes import crear_vista_clientes
from interfaz.compras import crear_vista_compras
from interfaz.libros import crear_vista_libros
from interfaz.estilos import aplicar_estilo_tabla


def iniciar_aplicacion():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("gotico.json")

    ventana = ctk.CTk()
    ventana.title("Sistema de Biblioteca")
    ventana.geometry("1000x650")

    aplicar_estilo_tabla()

    pestanas = ctk.CTkTabview(ventana)
    pestanas.pack(fill="both", expand=True, padx=15, pady=15)

    tab_libros = pestanas.add("Libros")
    tab_clientes = pestanas.add("Clientes")
    tab_compras = pestanas.add("Compras")

    actualizar_libros = crear_vista_libros(tab_libros)
    actualizar_clientes = crear_vista_clientes(tab_clientes)
    actualizar_compras = crear_vista_compras(tab_compras)

    def al_cambiar_pestana():
        actual = pestanas.get()
        if actual == "Libros":
            actualizar_libros()
        elif actual == "Clientes":
            actualizar_clientes()
        elif actual == "Compras":
            actualizar_compras()

    pestanas.configure(command=al_cambiar_pestana)

    ventana.mainloop()