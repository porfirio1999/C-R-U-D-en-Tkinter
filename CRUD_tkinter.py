import tkinter as tk
from tkinter import messagebox, ttk
from pymongo import MongoClient
from bson.objectid import ObjectId
import re  # Importar para realizar validaciones con expresiones regulares

# Conectar con MongoDB
cliente = MongoClient('mongodb://localhost:27017/')
bd = cliente['crud_bd']
coleccion = bd['usuarios']

# Variables globales
id_seleccionado = None  # Almacenará el ID del usuario seleccionado

# Funciones CRUD

def validar_entradas():
    """Valida que el campo Nombre solo contenga letras, el campo Edad sea un número entero positivo, 
    la CURP sea válida, el sexo sea 'M' o 'F', estatura y peso sean números positivos, y el lugar de nacimiento sea texto."""
    
    nombre = entrada_nombre.get()
    edad = entrada_edad.get()
    curp = entrada_curp.get()
    sexo = entrada_sexo.get().upper()
    estatura = entrada_estatura.get()
    peso = entrada_peso.get()
    lugar_nacimiento = entrada_lugar_nacimiento.get()

    # Verificar que el campo Nombre no esté vacío y contenga solo letras (sin números ni caracteres especiales)
    if not nombre:
        messagebox.showwarning("Advertencia", "El campo 'Nombre' no puede estar vacío.")
        return False

    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
        messagebox.showwarning("Advertencia", "El campo 'Nombre' solo puede contener letras y espacios.")
        return False

    # Verificar que el campo Edad sea un número entero positivo
    if not edad.isdigit() or int(edad) <= 0:
        messagebox.showwarning("Advertencia", "El campo 'Edad' debe ser un número entero positivo.")
        return False

    # Validar la CURP: Debe tener exactamente 18 caracteres y solo contener letras y números
    if not re.match(r"^[A-Z0-9]{18}$", curp.upper()):
        messagebox.showwarning("Advertencia", "El campo 'CURP' debe tener 18 caracteres y solo contener letras y números.")
        return False

    # Validar sexo: Solo "M" o "F"
    if sexo not in ['M', 'F']:
        messagebox.showwarning("Advertencia", "El campo 'Sexo' debe ser 'M' (Masculino) o 'F' (Femenino).")
        return False

    # Validar estatura: Debe ser un número positivo
    try:
        if float(estatura) <= 0:
            messagebox.showwarning("Advertencia", "El campo 'Estatura' debe ser un número positivo.")
            return False
    except ValueError:
        messagebox.showwarning("Advertencia", "El campo 'Estatura' debe ser un número válido.")
        return False

    # Validar peso: Debe ser un número positivo
    try:
        if float(peso) <= 0:
            messagebox.showwarning("Advertencia", "El campo 'Peso' debe ser un número positivo.")
            return False
    except ValueError:
        messagebox.showwarning("Advertencia", "El campo 'Peso' debe ser un número válido.")
        return False

    # Validar lugar de nacimiento: Solo letras y espacios
    if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", lugar_nacimiento):
        messagebox.showwarning("Advertencia", "El campo 'Lugar de Nacimiento' solo puede contener letras y espacios.")
        return False

    return True

def insertar_datos():
    if not validar_entradas():
        return

    nombre = entrada_nombre.get()
    edad = entrada_edad.get()
    curp = entrada_curp.get()
    sexo = entrada_sexo.get().upper()
    estatura = float(entrada_estatura.get())
    peso = float(entrada_peso.get())
    lugar_nacimiento = entrada_lugar_nacimiento.get()

    # Insertar datos sin ID (MongoDB lo genera automáticamente)
    coleccion.insert_one({"nombre": nombre, "edad": int(edad), "curp": curp, "sexo": sexo, "estatura": estatura, "peso": peso, "lugar_nacimiento": lugar_nacimiento})
    messagebox.showinfo("Éxito", "Datos insertados correctamente")
    mostrar_datos()
    limpiar_entradas()

def mostrar_datos():
    tabla.delete(*tabla.get_children())  # Limpiar tabla antes de mostrar
    filas = coleccion.find()
    for fila in filas:
        # Usa get() para manejar si el campo no existe
        curp = fila.get("curp", "No disponible")
        sexo = fila.get("sexo", "No disponible")
        estatura = fila.get("estatura", "No disponible")
        peso = fila.get("peso", "No disponible")
        lugar_nacimiento = fila.get("lugar_nacimiento", "No disponible")
        tabla.insert('', tk.END, values=(str(fila['_id']), fila['nombre'], fila['edad'], curp, sexo, estatura, peso, lugar_nacimiento))

def obtener_fila_seleccionada(event):
    # Verificar si hay algún elemento seleccionado
    if not tabla.selection():
        return  # No hay selección, salir de la función

    item = tabla.selection()[0]
    fila_seleccionada = tabla.item(item, 'values')

    # Guardar el ID seleccionado pero no mostrarlo en la interfaz
    global id_seleccionado
    id_seleccionado = fila_seleccionada[0]

    # Mostrar solo nombre, edad, curp, sexo, estatura, peso y lugar de nacimiento en las entradas
    entrada_nombre.delete(0, tk.END)
    entrada_nombre.insert(tk.END, fila_seleccionada[1])

    entrada_edad.delete(0, tk.END)
    entrada_edad.insert(tk.END, fila_seleccionada[2])
    
    entrada_curp.delete(0, tk.END)
    entrada_curp.insert(tk.END, fila_seleccionada[3])

    entrada_sexo.delete(0, tk.END)
    entrada_sexo.insert(tk.END, fila_seleccionada[4])

    entrada_estatura.delete(0, tk.END)
    entrada_estatura.insert(tk.END, fila_seleccionada[5])

    entrada_peso.delete(0, tk.END)
    entrada_peso.insert(tk.END, fila_seleccionada[6])

    entrada_lugar_nacimiento.delete(0, tk.END)
    entrada_lugar_nacimiento.insert(tk.END, fila_seleccionada[7])

def actualizar_datos():
    if not validar_entradas():
        return

    nombre = entrada_nombre.get()
    edad = entrada_edad.get()
    curp = entrada_curp.get()
    sexo = entrada_sexo.get().upper()
    estatura = float(entrada_estatura.get())
    peso = float(entrada_peso.get())
    lugar_nacimiento = entrada_lugar_nacimiento.get()

    try:
        coleccion.update_one({"_id": ObjectId(id_seleccionado)}, {"$set": {"nombre": nombre, "edad": int(edad), "curp": curp, "sexo": sexo, "estatura": estatura, "peso": peso, "lugar_nacimiento": lugar_nacimiento}})
        messagebox.showinfo("Éxito", "Datos actualizados correctamente")
        mostrar_datos()
        limpiar_entradas()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar: {str(e)}")

def eliminar_datos():
    if id_seleccionado is None:
        messagebox.showwarning("Advertencia", "Debe seleccionar un registro para eliminar")
        return

    try:
        coleccion.delete_one({"_id": ObjectId(id_seleccionado)})
        messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        mostrar_datos()
        limpiar_entradas()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")

def limpiar_entradas():
    entrada_nombre.delete(0, tk.END)
    entrada_edad.delete(0, tk.END)
    entrada_curp.delete(0, tk.END)
    entrada_sexo.delete(0, tk.END)
    entrada_estatura.delete(0, tk.END)
    entrada_peso.delete(0, tk.END)
    entrada_lugar_nacimiento.delete(0, tk.END)
    global id_seleccionado
    id_seleccionado = None  # Limpiar también el ID seleccionado

# Crear la interfaz de Tkinter

ventana = tk.Tk()
ventana.title("CRUD con Tkinter y MongoDB")
ventana.geometry("700x600")

# Campos de entrada (nombre, edad, curp, sexo, estatura, peso y lugar de nacimiento)
marco = tk.Frame(ventana)
marco.pack(pady=10)

etiqueta_nombre = tk.Label(marco, text="Nombre")
etiqueta_nombre.grid(row=0, column=0)
entrada_nombre = tk.Entry(marco)
entrada_nombre.grid(row=0, column=1)

etiqueta_edad = tk.Label(marco, text="Edad")
etiqueta_edad.grid(row=1, column=0)
entrada_edad = tk.Entry(marco)
entrada_edad.grid(row=1, column=1)

etiqueta_curp = tk.Label(marco, text="Curp")
etiqueta_curp.grid(row=2, column=0)
entrada_curp = tk.Entry(marco)
entrada_curp.grid(row=2, column=1)

etiqueta_sexo = tk.Label(marco, text="Sexo (M/F)")
etiqueta_sexo.grid(row=3, column=0)
entrada_sexo = tk.Entry(marco)
entrada_sexo.grid(row=3, column=1)

etiqueta_estatura = tk.Label(marco, text="Estatura (metros)")
etiqueta_estatura.grid(row=4, column=0)
entrada_estatura = tk.Entry(marco)
entrada_estatura.grid(row=4, column=1)

etiqueta_peso = tk.Label(marco, text="Peso (kg)")
etiqueta_peso.grid(row=5, column=0)
entrada_peso = tk.Entry(marco)
entrada_peso.grid(row=5, column=1)

etiqueta_lugar_nacimiento = tk.Label(marco, text="Lugar de Nacimiento")
etiqueta_lugar_nacimiento.grid(row=6, column=0)
entrada_lugar_nacimiento = tk.Entry(marco)
entrada_lugar_nacimiento.grid(row=6, column=1)

# Botones
marco_botones = tk.Frame(ventana)
marco_botones.pack(pady=10)

boton_insertar = tk.Button(marco_botones, text="Insertar", command=insertar_datos)
boton_insertar.grid(row=0, column=0, padx=5)

boton_actualizar = tk.Button(marco_botones, text="Actualizar", command=actualizar_datos)
boton_actualizar.grid(row=0, column=1, padx=5)

boton_eliminar = tk.Button(marco_botones, text="Eliminar", command=eliminar_datos)
boton_eliminar.grid(row=0, column=2, padx=5)

boton_limpiar = tk.Button(marco_botones, text="Limpiar", command=limpiar_entradas)
boton_limpiar.grid(row=0, column=3, padx=5)

# Tabla para mostrar datos
tabla = ttk.Treeview(ventana, columns=("ID", "Nombre", "Edad", "Curp", "Sexo", "Estatura", "Peso", "Lugar de Nacimiento"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.heading("Edad", text="Edad")
tabla.heading("Curp", text="Curp")
tabla.heading("Sexo", text="Sexo")
tabla.heading("Estatura", text="Estatura")
tabla.heading("Peso", text="Peso")
tabla.heading("Lugar de Nacimiento", text="Lugar de Nacimiento")
tabla.pack(pady=20)

tabla.bind('<ButtonRelease-1>', obtener_fila_seleccionada)

# Mostrar los datos inicialmente
mostrar_datos()

ventana.mainloop()
