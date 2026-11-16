"""Estilo oscuro (negro y rojo) para las tablas ttk.Treeview.

Las tablas no son de CustomTkinter, por eso no siguen el tema JSON
y hay que pintarlas aparte con ttk.Style.
"""

from tkinter import ttk

NEGRO = "#120808"
ROJO_SANGRE = "#B01212"
ROJO_OSCURO = "#8B1414"
TEXTO = "#FFFFFF"


def aplicar_estilo_tabla():
    estilo = ttk.Style()
    # "clam" es el único tema de ttk que respeta los colores de los encabezados.
    estilo.theme_use("clam")

    estilo.configure(
        "Treeview",
        background=NEGRO,
        fieldbackground=NEGRO,
        foreground=TEXTO,
        rowheight=32,
        borderwidth=0,
        font=("Segoe UI", 12),
    )
    estilo.configure(
        "Treeview.Heading",
        background=ROJO_OSCURO,
        foreground=TEXTO,
        relief="flat",
        font=("Segoe UI", 12, "bold"),
    )
    estilo.map(
        "Treeview",
        background=[("selected", ROJO_SANGRE)],
        foreground=[("selected", "#FFFFFF")],
    )
    estilo.map("Treeview.Heading", background=[("active", ROJO_SANGRE)])