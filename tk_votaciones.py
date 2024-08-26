# Realizado por Gonzalo Montezuma
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime, date
import random
import re
import os

# Configurar la conexión a la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="votaciones"
)

#CUI unico
def verificar_cui_unico(cui):
    mycursor = mydb.cursor()
    sql = "SELECT COUNT(*) FROM estudiantes_info WHERE CUI = %s"
    mycursor.execute(sql, (cui,))
    count = mycursor.fetchone()[0]
    return count == 0

#Generar CUI
def generar_numero():
    while True:
        numero = generar_segmento(4) + "-" + generar_segmento(5) + "-" + generar_segmento(4)
        if validar_numero(numero) and verificar_cui_unico(numero):
            return numero

#Segmentos CUI
def generar_segmento(length):
    segmento = [random.randint(1, 9) for _ in range(length)]
    for i in range(2, length):
        # Evitar tres números iguales seguidos
        if segmento[i] == segmento[i-1] == segmento[i-2]:
            segmento[i] = random.choice([x for x in range(1, 10) if x != segmento[i-1]])
        
        # Evitar tres números consecutivos seguidos (ascendente o descendente)
        if (segmento[i] == segmento[i-1] + 1 == segmento[i-2] + 2) or \
           (segmento[i] == segmento[i-1] - 1 == segmento[i-2] - 2):
            segmento[i] = random.choice([x for x in range(1, 10) if x not in {segmento[i-1] + 1, segmento[i-1] - 1}])

    return "".join(map(str, segmento))

#Validar dígitos CUI
def validar_numero(numero):
    segmentos = numero.split('-')
    for segmento in segmentos:
        for i in range(2, len(segmento)):
            if segmento[i] == segmento[i-1] == segmento[i-2]:
                return False
            if (int(segmento[i]) == int(segmento[i-1]) + 1 == int(segmento[i-2]) + 2) or \
               (int(segmento[i]) == int(segmento[i-1]) - 1 == int(segmento[i-2]) - 2):
                return False
    return True

# Función para ejecutar el comando SQL y mostrar los resultados
def ver(tabla):
    if tabla == "estudiantes_info":
        columns = ("ID", "CUI", "Nombres", "Apellidos", "Fecha Nacimiento", "Fecha Creación", "Fecha Vencimiento", 
               "Género", "Grado ID", "Edad", "Ya Votó")
        Stringyiyi = "SELECT * FROM estudiantes_info"
        # Configurar los encabezados del Treeview y ajustar el ancho de las columnas
        column_widths = {
        "ID": 30,
        "CUI": 120,
        "Nombres": 150,
        "Apellidos": 150,
        "Fecha Nacimiento": 100,
        "Fecha Creación": 100,
        "Fecha Vencimiento": 100,
        "Género": 50,
        "Grado ID": 50,
        "Edad": 50,
        "Ya Votó": 50
        }

    elif tabla == "registro":
        columns = ("ID", "Estudiante ID")
        Stringyiyi = "SELECT * FROM votos"

    else:
        return

    mycursor = mydb.cursor()
    mycursor.execute(Stringyiyi)
    myresult = mycursor.fetchall()

    # Crear una nueva ventana para mostrar los resultados
    results_window = tk.Toplevel()
    results_window.title(f"Datos - {tabla}")

    # Crear un Treeview para mostrar los resultados en formato de tabla
    tree = ttk.Treeview(results_window, columns=columns, show='headings')

    if tabla == "estudiantes_info":
        # Configurar los encabezados del Treeview
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=column_widths[col])
        
        # Insertar los datos en el Treeview
        for row in myresult:
            # Convertir 0 a "No" y 1 a "Sí" en la columna "Ya Votó"
            row = list(row)
            if row[-1] == 0:
                row[-1] = "No"
            elif row[-1] == 1:
                row[-1] = "Sí"
            tree.insert("", "end", values=row)
    
    elif tabla == "registro":
        # Configurar los encabezados del Treeview
        for col in columns:
            tree.heading(col, text=col)
        
        for row in myresult:
            tree.insert("", "end", values=row)

    tree.pack(expand=True, fill='both')

# Función para verificar si el ID del estudiante existe en la base de datos
def verificar_estudiante_id(id_estudiante):
    mycursor = mydb.cursor()
    sql = "SELECT COUNT(*) FROM estudiantes WHERE id_estudiante = %s"
    mycursor.execute(sql, (id_estudiante,))
    result = mycursor.fetchone()
    return result[0] > 0

# Función para abrir la ventana con opciones de tablas
def open_table_options():
    table_window = tk.Toplevel()
    table_window.title("Ver datos")
    table_window.geometry("250x100")
    table_window.resizable(False, False)

    estudiantes_button = tk.Button(table_window, text="Estudiantes", command=lambda: ver("estudiantes_info"))
    estudiantes_button.pack(pady=10)

    registro_button = tk.Button(table_window, text="Votos", command=lambda: ver("registro"))
    registro_button.pack(pady=10)

def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

# Función para crear un estudiante
def crear_estudiante(nombres_entry, apellidos_entry, fecha_nacimiento_entry, fecha_creacion_entry, fecha_vencimiento_entry, genero_var, grado_combobox, window, status_label):
    nombres = nombres_entry.get()
    apellidos = apellidos_entry.get()
    fecha_nacimiento = fecha_nacimiento_entry.get()
    fecha_creacion = fecha_creacion_entry.get()
    fecha_vencimiento = fecha_vencimiento_entry.get()
    genero = genero_var.get()
    grado = grado_combobox.get()

    if not (nombres and apellidos and fecha_nacimiento and fecha_creacion and fecha_vencimiento and genero and grado):
        messagebox.showerror("Error", "Todos los campos deben estar llenos.", parent=window)
        return

    if len(nombres) > 100:
        messagebox.showerror("Error", "El nombre supera los 100 caracteres, escriba una cadena más corta", parent=window)
        return
    if len(apellidos) > 100:
        messagebox.showerror("Error", "El apellido supera los 100 caracteres, escriba una cadena más corta", parent=window)
        return
    
    # Convertir las fechas de string a datetime.date
    try:
        fecha_nacimiento_dt = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        fecha_creacion_dt = datetime.strptime(fecha_creacion, '%Y-%m-%d').date()
        fecha_vencimiento_dt = datetime.strptime(fecha_vencimiento, '%Y-%m-%d').date()
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto.", parent=window)
        return
    
    # Calcular edad
    edad = calcular_edad(fecha_nacimiento_dt)
    
    # Mapa de grados (puede ajustarse según sea necesario)
    grados = {
        "Prepa_1": 1, "Prepa_2": 2, "Primero_Primaria 1": 3, "Primero_Primaria 2": 4,
        "Segundo_Primaria_1": 5, "Segundo_Primaria_2": 6, "Tercero_Primaria_1": 7, "Tercero_Primaria_2": 8,
        "Cuarto_Primaria_1": 9, "Cuarto_Primaria_2": 10, "Quinto_Primaria_1": 11, "Quinto_Primaria_2": 12,
        "Sexto_Primaria_1": 13, "Sexto_Primaria_2": 14, "Primero_Basico_1": 15, "Primero_Basico_2": 16,
        "Segundo_Basico_1": 17, "Segundo_Basico_2": 18, "Tercero_Basico_1": 19, "Tercero_Basico_2": 20,
        "Cuarto_CCLL_1": 21, "Cuarto_CCLL_2": 22, "Cuarto_BACO": 23, "Cuarto_BADI": 24,
        "Quinto_CCLL_1": 25, "Quinto_CCLL_2": 26, "Quinto_BACO": 27, "Quinto_BADI": 28
    }
    
    grado_id = grados.get(grado)

    if not grado_id:
        messagebox.showerror("Error", "Grado no válido.", parent=window)
        return

    numero_aleatorio = generar_numero()

    try:
        mycursor = mydb.cursor()
        sql = "INSERT INTO estudiantes_info (nombres, apellidos, fecha_nacimiento, fecha_creacion, fecha_vencimiento, genero, grado_id, edad, ya_voto, CUI) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (nombres, apellidos, fecha_nacimiento_dt, fecha_creacion_dt, fecha_vencimiento_dt, genero, grado_id, edad, 0, numero_aleatorio)
        mycursor.execute(sql, val)
        mydb.commit()

        status_label.config(text="Estudiante creado exitosamente")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el estudiante: {e}", parent=window)
    finally:
        # Limpiar las cajas de texto después de crear el estudiante
        nombres_entry.delete(0, tk.END)
        apellidos_entry.delete(0, tk.END)
        genero_var.set(None)
        grado_combobox.set('')
        fecha_nacimiento_entry.set_date(date.today())
        fecha_creacion_entry.set_date(date.today())
        fecha_vencimiento_entry.set_date(date.today())

        # Establecer el foco en la caja de texto del nombre
        nombres_entry.focus_set()

# Función para abrir la ventana para crear un estudiante
def open_create_student():
    create_window = tk.Toplevel()
    create_window.title("Crear Estudiante")
    create_window.geometry("400x600")
    create_window.resizable(False, False)

    tk.Label(create_window, text="Ingrese los nombres del estudiante:").pack(pady=5)
    nombres_entry = tk.Entry(create_window)
    nombres_entry.pack(pady=5)

    tk.Label(create_window, text="Ingrese los apellidos del estudiante:").pack(pady=5)
    apellidos_entry = tk.Entry(create_window)
    apellidos_entry.pack(pady=5)

    tk.Label(create_window, text="Seleccione la fecha de nacimiento:").pack(pady=5)
    fecha_nacimiento_entry = DateEntry(create_window, date_pattern='yyyy-mm-dd')
    fecha_nacimiento_entry.pack(pady=5)

    tk.Label(create_window, text="Seleccione la fecha de creación:").pack(pady=5)
    fecha_creacion_entry = DateEntry(create_window, date_pattern='yyyy-mm-dd')
    fecha_creacion_entry.pack(pady=5)

    tk.Label(create_window, text="Seleccione la fecha de vencimiento:").pack(pady=5)
    fecha_vencimiento_entry = DateEntry(create_window, date_pattern='yyyy-mm-dd')
    fecha_vencimiento_entry.pack(pady=5)

    tk.Label(create_window, text="Seleccione el género:").pack(pady=5)
    genero_var = tk.StringVar()
    tk.Radiobutton(create_window, text="Masculino", variable=genero_var, value="M").pack(pady=5)
    tk.Radiobutton(create_window, text="Femenino", variable=genero_var, value="F").pack(pady=5)

    tk.Label(create_window, text="Seleccione el grado:").pack(pady=5)
    grados = [
        "Prepa_1", "Prepa_2", "Primero_Primaria 1", "Primero_Primaria 2", "Segundo_Primaria_1", "Segundo_Primaria_2",
        "Tercero_Primaria_1", "Tercero_Primaria_2", "Cuarto_Primaria_1", "Cuarto_Primaria_2", "Quinto_Primaria_1", 
        "Quinto_Primaria_2", "Sexto_Primaria_1", "Sexto_Primaria_2", "Primero_Basico_1", "Primero_Basico_2", 
        "Segundo_Basico_1", "Segundo_Basico_2", "Tercero_Basico_1", "Tercero_Basico_2", "Cuarto_CCLL_1", "Cuarto_CCLL_2", 
        "Cuarto_BACO", "Cuarto_BADI", "Quinto_CCLL_1", "Quinto_CCLL_2", "Quinto_BACO", "Quinto_BADI"
    ]
    grado_combobox = ttk.Combobox(create_window, values=grados, state='readonly')
    grado_combobox.pack(pady=5)

    status_label = tk.Label(create_window, text="")
    status_label.pack(pady=5)

    create_button = tk.Button(create_window, text="Crear", 
                              command=lambda: crear_estudiante(nombres_entry, apellidos_entry, fecha_nacimiento_entry, fecha_creacion_entry, fecha_vencimiento_entry, genero_var, grado_combobox, create_window, status_label))
    create_button.pack(pady=20)

    # Establecer el foco inicial en la caja de texto del nombre
    nombres_entry.focus_set()

    # Establecer el valor de la variable genero_var en None para asegurar que ningún botón esté seleccionado inicialmente
    genero_var.set(None)

# Verificar si el ID del estudiante existe en la base de datos
def verificar_estudiante_id(id_estudiante):
    mycursor = mydb.cursor()
    sql = "SELECT COUNT(*) FROM estudiantes WHERE id_estudiante = %s"
    mycursor.execute(sql, (id_estudiante,))
    result = mycursor.fetchone()
    return result[0] > 0

# Verificar el formato del CUI
def verificar_formato_cui(cui):
    pattern = r'^\d{4}-\d{5}-\d{4}$'
    return re.match(pattern, cui) is not None

# Obtener el ID del estudiante basado en CUI o ID
def obtener_estudiante(identificacion, tipo):
    cursor = mydb.cursor()
    if tipo == 'CUI':
        query = "SELECT id_estudiante, ya_voto FROM estudiantes_info WHERE CUI = %s"
    else:  # tipo == 'ID_ESTUDIANTE'
        query = "SELECT id_estudiante, ya_voto FROM estudiantes_info WHERE id_estudiante = %s"
    cursor.execute(query, (identificacion,))
    resultado = cursor.fetchone()
    return resultado  # Devuelve None si no existe

#Registrar voto
def registrar_voto(identificacion_entry, partido_var, tipo_var, window, status_label):
    identificacion = identificacion_entry.get().strip()
    partido = partido_var.get()
    tipo = tipo_var.get()

    if not identificacion or not partido:
        messagebox.showerror("Error", "Todos los campos deben estar llenos.", parent=window)
        return

    # Validar la identificación según el tipo seleccionado
    if tipo == "CUI":
        if not verificar_formato_cui(identificacion):
            messagebox.showerror("Error", "CUI no válido. Debe tener el formato ####-#####-####.", parent=window)
            return
    else:  # tipo == "ID_ESTUDIANTE"
        if not identificacion.isdigit():
            messagebox.showerror("Error", "El ID del estudiante debe ser un número entero válido.", parent=window)
            return
        identificacion = int(identificacion)

    # Obtener información del estudiante
    estudiante_info = obtener_estudiante(identificacion, tipo)

    # Verificación de que el estudiante existe
    if estudiante_info is None:
        messagebox.showerror("Error", f"El {tipo} ingresado no existe en la base de datos.", parent=window)
        return

    id_estudiante, ya_voto = estudiante_info

    if ya_voto == 1:
        messagebox.showerror("Error", "El estudiante ya ha registrado su voto.", parent=window)
        return

    try:
        cursor = mydb.cursor()

        # Actualizar la tabla "partidos" incrementando No_votos para el partido seleccionado
        sql_update_partido = "UPDATE partidos SET No_votos = No_votos + 1 WHERE nombre = %s"
        cursor.execute(sql_update_partido, (partido,))

        # Actualizar el campo "ya_voto" en la tabla "estudiantes"
        sql_update_estudiante = "UPDATE estudiantes_info SET ya_voto = 1 WHERE id_estudiante = %s"
        cursor.execute(sql_update_estudiante, (id_estudiante,))

        # Insertar el voto en la tabla "votos"
        sql_insert_voto = "INSERT INTO votos (id_estudiante) VALUES (%s)"
        cursor.execute(sql_insert_voto, (id_estudiante,))

        # Confirmar los cambios en la base
        mydb.commit()

        status_label.config(text="Voto registrado exitosamente", fg="green")

        # Limpiar las entradas después de registrar el voto
        identificacion_entry.delete(0, tk.END)
        partido_var.set(None)
        tipo_var.set("CUI")
        identificacion_entry.focus_set()

    except Exception as e:
        mydb.rollback()
        messagebox.showerror("Error", f"No se pudo registrar el voto: {e}", parent=window)

# Función para abrir la ventana para registrar un voto
def open_register_vote():
    vote_window = tk.Toplevel()
    vote_window.title("Registrar Voto")
    vote_window.geometry("400x600")
    vote_window.resizable(False, False)

    # Tipo de identificación
    tipo_frame = tk.Frame(vote_window)
    tipo_frame.pack(pady=10)

    tk.Label(tipo_frame, text="Seleccione el tipo de identificación:").pack(anchor="w")

    tipo_var = tk.StringVar(value="CUI")
    tk.Radiobutton(tipo_frame, text="CUI", variable=tipo_var, value="CUI", command=lambda: actualizar_label()).pack(anchor="w")
    tk.Radiobutton(tipo_frame, text="ID_ESTUDIANTE", variable=tipo_var, value="ID_ESTUDIANTE", command=lambda: actualizar_label()).pack(anchor="w")

    # Entrada de identificación
    identificacion_frame = tk.Frame(vote_window)
    identificacion_frame.pack(pady=10)

    identificacion_label = tk.Label(identificacion_frame, text="Ingrese el CUI:")
    identificacion_label.pack(anchor="w")

    identificacion_entry = tk.Entry(identificacion_frame, width=30)
    identificacion_entry.pack()

    # Selección de partido
    partido_frame_superior = tk.Frame(vote_window)
    partido_frame_superior.pack(pady=10)

    partido_frame_inferior = tk.Frame(vote_window)
    partido_frame_inferior.pack(pady=10)

    tk.Label(partido_frame_superior, text="Seleccione el partido:").grid(row=0, columnspan=2)

    partido_var = tk.StringVar()
    partidos = obtener_partidos_disponibles()

    if not partidos:
        messagebox.showerror("Error", "No hay partidos disponibles en la base de datos.", parent=vote_window)
        vote_window.destroy()
        return

    # Colocar los partidos 1 y 2 uno al lado del otro
    for i, partido in enumerate(partidos[:2]):
        nombre_archivo = f"{partido.replace(' ', '_')}.png"
        ruta_imagen = os.path.join("imagenes", nombre_archivo)
        
        print(f"Intentando cargar la imagen desde: {ruta_imagen}")

        try:
            image = Image.open(ruta_imagen)
            image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"No se pudo cargar la imagen para el partido {partido}: {e}")
            photo = None

        tk.Radiobutton(partido_frame_superior, text=partido, variable=partido_var, value=partido).grid(row=1, column=i, sticky="w")

        if photo:
            image_label = tk.Label(partido_frame_superior, image=photo)
            image_label.image = photo
            image_label.grid(row=2, column=i, pady=5)

    # Colocar el partido 3 debajo de los partidos 1 y 2
    if len(partidos) > 2:
        partido = partidos[2]
        nombre_archivo = f"{partido.replace(' ', '_')}.png"
        ruta_imagen = os.path.join("imagenes", nombre_archivo)
        
        print(f"Intentando cargar la imagen desde: {ruta_imagen}")

        try:
            image = Image.open(ruta_imagen)
            image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"No se pudo cargar la imagen para el partido {partido}: {e}")
            photo = None

        tk.Radiobutton(partido_frame_inferior, text=partido, variable=partido_var, value=partido).pack(anchor="w")

        if photo:
            image_label = tk.Label(partido_frame_inferior, image=photo)
            image_label.image = photo
            image_label.pack(pady=5)

    # Botón de votar
    votar_button = tk.Button(vote_window, text="Votar", width=20,
                             command=lambda: registrar_voto(identificacion_entry, partido_var, tipo_var, vote_window, status_label))
    votar_button.pack(pady=20)

    # Etiqueta de estado
    status_label = tk.Label(vote_window, text="", fg="red")
    status_label.pack()

    # Función para actualizar el texto del label de identificación
    def actualizar_label():
        if tipo_var.get() == "CUI":
            identificacion_label.config(text="Ingrese el CUI:")
        else:
            identificacion_label.config(text="Ingrese el ID del estudiante:")
        identificacion_entry.delete(0, tk.END)
        identificacion_entry.focus_set()

    # Enfocar la entrada de identificación al abrir la ventana
    identificacion_entry.focus_set()

    partido_var.set(None)
    tipo_var.set(None)

# Función para obtener la lista de partidos disponibles desde la base de datos
def obtener_partidos_disponibles():
    cursor = mydb.cursor()
    cursor.execute("SELECT nombre FROM partidos")
    resultados = cursor.fetchall()
    return [resultado[0] for resultado in resultados]

# Función para abrir las opciones de creación
def open_create_options():
    create_options_window = tk.Toplevel()
    create_options_window.title("Ingresar Datos")
    create_options_window.geometry("250x100")
    create_options_window.resizable(False, False)

    estudiantes_button = tk.Button(create_options_window, text="Estudiantes", command=open_create_student)
    estudiantes_button.pack(pady=10)

    votar_button = tk.Button(create_options_window, text="Votar", command=open_register_vote)
    votar_button.pack(pady=10)

def mostrar_cuenta_votos():
    # Crear una nueva ventana
    votos_window = tk.Toplevel()
    votos_window.title("Cuenta de Votos en Vivo")
    votos_window.geometry("600x430")
    votos_window.resizable(False, False)

    # Obtener la información de los partidos
    mycursor = mydb.cursor()
    mycursor.execute("SELECT nombre, presidente, vice_presidente, No_Votos FROM partidos")
    partidos = mycursor.fetchall()

    votos_labels = []  # Lista para almacenar los labels de votos

    for partido in partidos:
        nombre, presidente, vicepresidente, no_votos = partido
        
        # Crear un frame para cada partido
        frame_partido = tk.Frame(votos_window)
        frame_partido.pack(pady=10, anchor='w', padx=20)

        # Cargar la imagen del partido
        nombre_archivo = f"{nombre.replace(' ', '_')}.png"
        ruta_imagen = os.path.join("imagenes", nombre_archivo)
        try:
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((100, 100))
            imagen = ImageTk.PhotoImage(imagen)
            label_imagen = tk.Label(frame_partido, image=imagen)
            label_imagen.image = imagen
            label_imagen.grid(row=0, column=0, rowspan=4, padx=10)
        except Exception as e:
            print(f"No se pudo cargar la imagen para el partido {nombre}: {e}")

        # Mostrar la información del partido
        tk.Label(frame_partido, text=f"{nombre}", font=("Allan", 17,)).grid(row=0, column=1, sticky='w')
        tk.Label(frame_partido, text=f"Presidente: {presidente}", font=("Arial", 12)).grid(row=1, column=1, sticky='w')
        tk.Label(frame_partido, text=f"Vicepresidente: {vicepresidente}", font=("Arial", 12)).grid(row=2, column=1, sticky='w')
        tk.Label(frame_partido, text="Votos:", font=("Arial", 12)).grid(row=3, column=1, sticky='w')

        # Mostrar la cantidad de votos en grande y en rojo
        votos_label = tk.Label(frame_partido, text=no_votos, font=("Arial", 20, "bold"), fg="red")
        votos_label.grid(row=3, column=2, sticky='w')
        votos_labels.append(votos_label)  # Añadir el label a la lista

    # Función para actualizar la cuenta de votos en vivo
    def actualizar_votos():
        mycursor.execute("SELECT Nombre, No_votos FROM partidos")
        updated_partidos = mycursor.fetchall()
        for i, (_, No_Votos) in enumerate(updated_partidos):
            votos_labels[i].config(text=No_Votos)
        votos_window.after(1000, actualizar_votos)  # Actualizar cada segundo

    # Iniciar la actualización en vivo
    actualizar_votos()

# Configurar la ventana principal
root = tk.Tk()
root.title("Sistema de Votaciones")
root.geometry("300x200")
root.resizable(False, False)

ver_button = tk.Button(root, text="Ver datos", command=open_table_options)
ver_button.pack(pady=20)

crear_button = tk.Button(root, text="Ingresar datos", command=open_create_options)
crear_button.pack(pady=20)

stream_button = tk.Button(root, text="¡Votos en vivo!", command=mostrar_cuenta_votos)
stream_button.pack(pady=20)

root.mainloop()