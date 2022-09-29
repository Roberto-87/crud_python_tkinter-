from ast import Delete
from cProfile import label
from calendar import c
from cgitb import text
from logging.config import valid_ident
from mailbox import mbox
import numbers
import sqlite3
from tkinter import *
from tkinter import colorchooser
from tkinter import ttk
import re
import tkinter.messagebox as mbox
from tkinter import messagebox
import re
from turtle import xcor

ingreso = []
mi_id = 0


def crea_bd():
    bd_clientes = sqlite3.connect("base_clientes.db")
    return bd_clientes


def crea_tabla(bd_clientes):
    cursor = bd_clientes.cursor()
    try:
        sql = "CREATE TABLE clientes(id integer primary key AUTOINCREMENT , codigo integer, razon_social text, cuit integer, direccion text, condicion integer)"
        cursor.execute(sql)
        bd_clientes.commit()
    except:
        pass


bd_clientes = crea_bd()
crea_tabla(bd_clientes)
# ingresa_datos(bd_clientes, "cliente ingresado")


def background_color():
    global colores
    colores = colorchooser.askcolor()[1]
    root.config(background=colores)


# hace un select a la base de datos pidiendo el último id, el número más alto, y luego lo retorna sumandole 1
def get_last_id():
    cursor = bd_clientes.cursor()
    sql = "SELECT MAX(id) FROM clientes"
    cursor.execute(sql)
    bd_clientes.commit()
    rows = cursor.fetchall()
    for row in rows:
        last_id_bd = int(row[0])
        last_id = last_id_bd + 1
        return last_id


def alta(codigo, razon_social, cuit, direccion, condicion_pago):
    last_id = get_last_id()
    cliente_duplicado = control_cliente(codigo, razon_social, cuit)
    confirmar_alta = mbox.askyesno(
        "confirmación alta", "Desea continuar con el alta del cliente?"
    )

    if confirmar_alta and cliente_duplicado == None:
        data = (
            last_id,
            codigo.get(),
            razon_social.get(),
            cuit.get(),
            direccion.get(),
            condicion_pago.get(),
        )
        cuit = cuit.get()
        cuit_regex = valida_cuit(cuit)
        if cuit_regex == True:
            cursor = bd_clientes.cursor()
            sql = "INSERT INTO clientes(id, codigo, razon_social, cuit, direccion, condicion) VALUES(?,?,?,?,?,?)"

            cursor.execute(sql, data)
            bd_clientes.commit()
            mbox.showinfo("Confirmación alta", "Cliente creado correctamente")
            tree_update()  # muestra el nuevo cliente creado en el tree
            clear_form()
        else:
            messagebox.showerror(
                "error",
                "CUIT invalido: \n debe comenzar con el número 30 seguido de nueve cifras",
            )

    elif confirmar_alta == False:
        return
    elif cliente_duplicado != None:
        messagebox.showerror("error", "cliente existente")
        consulta(
            codigo, razon_social, cuit, condicion_pago
        )  # muestra en el tree el cliente que se quiso dar de alta y ya existe


def clear_form():  # limpia las entradas
    # codigo.set(""),
    razon_social.set(""),
    cuit.set(""),
    direccion.set(""),
    condicion_pago.set("")


def valida_cuit(cuit):
    solo_numeros = re.compile(r"^30\d{9}")
    mi_cuit = cuit

    if re.match(solo_numeros, str(mi_cuit)):
        return True
    else:
        return False


def tree_update():
    tree.delete(*tree.get_children())

    cursor = bd_clientes.cursor()
    sql = "SELECT * FROM clientes ORDER BY id DESC "
    cursor.execute(sql)
    bd_clientes.commit()
    elementos = cursor.fetchall()
    for elemento in elementos:

        tree.insert(
            "",
            "end",
            text=elemento[0],
            values=(
                elemento[1],
                elemento[2],
                elemento[3],
                elemento[4],
                elemento[5],
            ),
        ),


def control_cliente(
    codigo, razon_social, cuit
):  # se utiliza en diferentes funciones para validar si un cliente ya existe o no al momento de hacer una operación
    cursor = bd_clientes.cursor()
    sql = "SELECT * FROM clientes WHERE codigo=? or razon_social=? or cuit=?"
    data = (codigo.get(), razon_social.get(), cuit.get())
    cursor.execute(sql, data)
    bd_clientes.commit()
    clientes = cursor.fetchall()
    for cliente in clientes:
        if len(cliente) > 0:
            return False
        elif len(cliente) == 0 or len(cliente) == None:
            return True


def borrar_fila():
    global mi_id
    mi_id -= 1
    item_eliminado = tree.focus()
    tree.delete(item_eliminado)


def modificacion(razon_social, cuit, direccion, condicion_pago, codigo):

    cliente_inexistente = control_cliente(codigo, razon_social, cuit)
    if cliente_inexistente == False:
        cursor = bd_clientes.cursor()
        sql = "UPDATE clientes SET razon_social=?, cuit=?, direccion=?, condicion=? WHERE codigo=?;"
        data = (
            razon_social.get(),
            cuit.get(),
            direccion.get(),
            condicion_pago.get(),
            codigo.get(),
        )
        cuit_control = valida_cuit(cuit.get())
        if cuit_control == True:
            cursor.execute(sql, data)
            bd_clientes.commit()
            mbox.showinfo("Modificación", "Cliente modificado correctamente")
            consulto_cliente_actualizado(codigo)
            clear_form()
        else:
            messagebox.showerror(
                "error",
                "CUIT invalido: \n debe comenzar con el número 30 seguido de nueve cifras",
            )
    else:
        messagebox.showerror("error", "cliente inexistente")


def consulto_cliente_actualizado(codigo):
    cursor = bd_clientes.cursor()
    sql = "SELECT * FROM clientes WHERE codigo=?"
    bd_clientes.commit()
    data = (codigo.get(),)
    respuesta_bd = cursor.execute(sql, data)
    for elemento in respuesta_bd:
        tree.insert(
            "",
            "end",
            text=elemento[0],
            values=(
                elemento[1],
                elemento[2],
                elemento[3],
                elemento[4],
                elemento[5],
            ),
        )


def consulta(codigo, razon_social, cuit, condicion_pago):
    cliente_inexistente = control_cliente(codigo, razon_social, cuit)
    if cliente_inexistente == False:
        cursor = bd_clientes.cursor()
        info = (
            codigo.get(),
            razon_social.get(),
            cuit.get(),
            condicion_pago.get(),
        )
        sql = "SELECT * FROM clientes WHERE codigo=? or razon_social=? or cuit=? or condicion=?"
        respuesta_bd = cursor.execute(sql, info)
        for elemento in respuesta_bd:
            tree.insert(
                "",
                "end",
                text=elemento[0],
                values=(
                    elemento[1],
                    elemento[2],
                    elemento[3],
                    elemento[4],
                    elemento[5],
                ),
            )
    else:
        messagebox.showerror("error", "cliente inexistente")


def eliminar_cliente(codigo, razon_social, cuit):
    confirmar_baja = mbox.askyesno("confirmación baja", "Desea continuar?")
    cliente_inexistente = control_cliente(codigo, razon_social, cuit)
    if confirmar_baja and cliente_inexistente == False:
        cursor = bd_clientes.cursor()
        sql = "DELETE FROM clientes WHERE codigo=? or razon_social=? or cuit=?"
        data = (codigo.get(), razon_social.get(), cuit.get())
        cursor.execute(sql, data)
        bd_clientes.commit()
        mbox.showinfo("Confirmación baja", "Cliente eliminado correctamente")
        tree_update()
        clear_form()
    else:
        messagebox.showerror("error", "cliente inexistente")


def master_data():  # muestra todos los clientes ingresados en la base
    tree_update()


def previsualizar(codigo):
    cursor = bd_clientes.cursor()
    sql = "SELECT * FROM clientes WHERE codigo=?"
    bd_clientes.commit()
    data = (codigo.get(),)
    respuesta_bd = cursor.execute(sql, data)
    cliente_inexistente = control_cliente(codigo, razon_social, cuit)

    for elemento in respuesta_bd:
        if (
            entry_nombre.insert(0, elemento[2]) == ""
        ):  # si la entrada no tiene información hacer la inserción. En caso contrario, si se vuelve a presionar previsualizar, no dupliques la información, borrá los campos y traela nuevamente de la base de datos.
            entry_nombre.insert(0, elemento[2])
            entry_cuit.insert(0, elemento[3])
            entry_direccion.insert(0, elemento[4])
            entry_condicion.insert(0, elemento[5])
        elif entry_nombre.insert(0, elemento[2]) != "":
            clear_form()
            cursor = bd_clientes.cursor()
            sql = "SELECT * FROM clientes WHERE codigo=?"
            bd_clientes.commit()
            data = (codigo.get(),)
            respuesta_bd = cursor.execute(sql, data)
            entry_nombre.insert(0, elemento[2])
            entry_cuit.insert(0, elemento[3])
            entry_direccion.insert(0, elemento[4])
            entry_condicion.insert(0, elemento[5])


def limpiar_prev():
    clear_form()


def control_previsualizacion():
    cursor = bd_clientes.cursor()
    sql = "SELECT * FROM clientes WHERE codigo=?"
    bd_clientes.commit()
    data = (codigo.get(),)
    respuesta_bd = cursor.execute(sql, data)
    for elemento in respuesta_bd:
        entry_nombre.insert(0, elemento[2])
        entry_cuit.insert(0, elemento[3])
        entry_direccion.insert(0, elemento[4])
        entry_condicion.insert(0, elemento[5])


def borrar_tree():
    tree.delete(*tree.get_children())
    limpiar_prev()


##############################################################################################

root = Tk()
tree = ttk.Treeview(root)
colores = ""
root.geometry("850x500+200+100")
root.title("ABM- Clientes")

codigo, razon_social, cuit, direccion, condicion_pago = (
    StringVar(),
    StringVar(),
    StringVar(),
    StringVar(),
    StringVar(),
)


ingrese_datos = Label(
    root,
    text="ingrese sus datos",
)
ingrese_datos.grid(row=1, columnspan=20)
ingrese_datos.config(background="grey", width=85)

entry_codigo = Entry(textvariable=codigo)
entry_codigo.grid(row=2, column=2)
my_id = Label(root, text="Codigo")
my_id.grid(row=2, column=1, sticky=W)


entry_nombre = Entry(textvariable=razon_social)
entry_nombre.grid(row=3, column=2)
nombre = Label(root, text="Razón Social")
nombre.grid(row=3, column=1, sticky=W)

entry_cuit = Entry(textvariable=cuit)
entry_cuit.grid(row=4, column=2)
cuit_label = Label(root, text="CUIT")
cuit_label.grid(row=4, column=1, sticky=W)

entry_direccion = Entry(textvariable=direccion)
entry_direccion.grid(row=5, column=2)
direccion_label = Label(root, text="Direccion")
direccion_label.grid(row=5, column=1, sticky=W)

entry_condicion = Entry(textvariable=condicion_pago)
entry_condicion.grid(row=6, column=2)
condicion_label = Label(root, text="Condición de pago")
condicion_label.grid(row=6, column=1, sticky=W)


boton_alta = Button(
    root,
    text="Alta",
    command=lambda: alta(codigo, razon_social, cuit, direccion, condicion_pago),
)
boton_alta.grid(row=9, column=1)

boton_consultar = Button(
    root,
    text="Consultar",
    command=lambda: consulta(codigo, razon_social, cuit, condicion_pago),
)
boton_consultar.grid(row=9, column=2)

boton_consultar_todos = Button(
    root,
    text="Master Data",
    command=lambda: master_data(),
)
boton_consultar_todos.grid(row=9, column=3)

boton_previsualizar = Button(
    root,
    text="Previsualizar",
    command=lambda: previsualizar(codigo),
)
boton_previsualizar.grid(row=2, column=3)


boton_limpiar_prev = Button(
    root, text="Limpiar Previsualización", command=lambda: limpiar_prev()
)
boton_limpiar_prev.grid(row=2, column=4)

boton_modificar = Button(
    root,
    text="Modificar",
    command=lambda: modificacion(razon_social, cuit, direccion, condicion_pago, codigo),
)
boton_modificar.grid(row=9, column=4)

boton_borrar = Button(root, text="Borrar selección", command=lambda: borrar_fila())
boton_borrar.grid(row=9, column=5)

boton_limpiar_tree = Button(
    root, text="Limpiar pantalla", command=lambda: borrar_tree()
)
boton_limpiar_tree.grid(row=9, column=6)


boton_fondo = Button(root, text="Personalizar", command=lambda: background_color())
boton_fondo.grid(row=9, column=7)

boton_salir = Button(root, text="Salir", command=root.quit)
boton_salir.grid(row=10, column=10)

boton_salir = Button(
    root,
    text="Eliminar cliente",
    command=lambda: eliminar_cliente(codigo, razon_social, cuit),
)
boton_salir.grid(row=9, column=9)

tree = ttk.Treeview(root)
tree["columns"] = ("col1", "col2", "col3", "col4", "col5")
tree.column("#0", width=80, minwidth=80, anchor=W)
tree.column("col1", width=80, minwidth=80, anchor=W)
tree.column("col2", width=80, minwidth=80, anchor=W)
tree.column("col3", width=80, minwidth=80, anchor=W)
tree.column("col4", width=80, minwidth=80, anchor=W)
tree.column("col5", width=80, minwidth=80, anchor=W)

tree.heading("#0", text="Id")
tree.heading("col1", text="Codigo")
tree.heading("col2", text="Razón Social")
tree.heading("col3", text="CUIT")
tree.heading("col4", text="Dirección")
tree.heading("col5", text="Condición de pago")

tree.grid(column=1, row=8, columnspan=10)

##############################################################################################
root.mainloop()
