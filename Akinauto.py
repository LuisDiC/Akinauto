import mariadb
import random
from dotenv import load_dotenv
import os
import tkinter as tk
from tkinter import messagebox
from ctypes import windll

# Variables globales
columna_global = None
dato_global = None
PreguntasRealizadas = list()

# Cargar variables del entorno
load_dotenv()

# Conexión a la base de datos
conexion = mariadb.connect(
    host=os.getenv('HOST'),
    user=os.getenv('USER'),
    password=os.getenv('PASS'),
    database=os.getenv('DATABASE')
)
cursor = conexion.cursor(dictionary=True)

# Crear ventana principal
ventana = tk.Tk()
ventana.iconbitmap('./src/icon/AkinautoLentes.ico')
ventana.title("Akinauto")
ventana.geometry("500x400")


# Variables de texto
pregunta_var = tk.StringVar()
Nombre_var = tk.StringVar()

def inicializar_estado():
    cursor.execute("UPDATE carros SET estado = 1")
    PreguntasRealizadas.clear()
    conexion.commit()
    print("Estado inicializado: todas las filas tienen estado = 1")

inicializar_estado()

def realizar_pregunta():

    global columna_global, dato_global  
    consulta = "SELECT * FROM carros WHERE estado = 1"
    cursor.execute(consulta)
    filas = cursor.fetchall()

    if not filas: 
        messagebox.showinfo("Sin datos", "No hay carros con estado = 1 en la base de datos.")
        ventana.destroy()
        return

    if len(filas) == 1:  
        fila = filas[0]
        nombre = fila["Nombre"]
        mensaje = f"Tu carro es {nombre}. ¿Adiviné?"
        respuesta = messagebox.askquestion("Pregunta", mensaje)
        if respuesta == "yes":
            jugar_otra_vez = messagebox.askyesno("¡Te Gané!", "¡Me alegra haber jugado contigo!\n¿Quieres jugar otra vez?")
            if jugar_otra_vez:
                reiniciar_juego()
            else:
                ventana.destroy()
        
        else:
            Ingresar_Datos = messagebox.askyesno("¡Me ganaste!", "¿Puedes ingresar el carro y sus caracteristicas para recordarlo la próxima vez?")
            if Ingresar_Datos:
                Aprendizaje()
            else:
                jugar_otra_vez = messagebox.askyesno('Ni modo :C','¿Quieres jugar otra vez?')
                if jugar_otra_vez:
                    reiniciar_juego()
                else:
                    ventana.destroy()
    else:
        fila_aleatoria = random.choice(filas)
        columnas_validas = [col for col in fila_aleatoria.keys() if col != "estado"]
        columna_global = random.choice(columnas_validas) 
        dato_global = fila_aleatoria[columna_global]

        while dato_global in PreguntasRealizadas:
            print(PreguntasRealizadas)
            print('Se intento repetir ', dato_global)
            fila_aleatoria = random.choice(filas)
            columnas_validas = [col for col in fila_aleatoria.keys() if col != "estado"]
            columna_global = random.choice(columnas_validas) 
            dato_global = fila_aleatoria[columna_global]

        if not dato_global or dato_global == '':
            dato_global = "Desconocido"

        print(f"Columna seleccionada: {columna_global}, Dato seleccionado: {dato_global}")
        pregunta_var.set(f'¿Tu carro tiene {columna_global} "{dato_global}"?')
        PreguntasRealizadas.append(dato_global)

def responder_si():
    """
    Maneja la respuesta afirmativa a la pregunta actual.
    """
    manejar_respuesta(True)

def responder_no():
    """
    Maneja la respuesta negativa a la pregunta actual.
    """
    manejar_respuesta(False)

def manejar_respuesta(es_positivo):
    """
    Actualiza el estado de los registros en la base de datos según la respuesta del usuario.
    """
    global columna_global, dato_global

    print(f"Columna seleccionada: {columna_global}, Valor seleccionado: {dato_global}")

    if not columna_global or not dato_global or dato_global == '':
        messagebox.showerror("Error", "Columna o valor no válidos.")
        return

    try:
        if es_positivo:  # Respuesta "Sí"
            cursor.execute(f"UPDATE carros SET estado = 0 WHERE `{columna_global}` != %s", (dato_global,))
        else:  # Respuesta "No"
            cursor.execute(f"UPDATE carros SET estado = 0 WHERE `{columna_global}` = %s", (dato_global,))
        conexion.commit()

        print(f"Filas afectadas: {cursor.rowcount}")
        realizar_pregunta()
    except Exception as e:
        messagebox.showerror("Error en la consulta SQL", f"Ocurrió un error: {e}")

def reiniciar_juego():
    """
    Reinicia el estado de todos los registros al valor inicial (estado = 1).
    """
    PreguntasRealizadas.clear()
    cursor.execute("UPDATE carros SET estado = 1")
    conexion.commit()
    realizar_pregunta()



def Aprendizaje():
    Ventana_Aprendizaje = tk.Toplevel(ventana)
    Ventana_Aprendizaje.iconbitmap('./src/icon/AkinautoLentes.ico')
    Ventana_Aprendizaje.title("Nuevo Carro Aprendizaje")

    Texto_Aprendizaje = tk.Label(Ventana_Aprendizaje, text = "Ingresa el nuevo vehiculo")
    Texto_Aprendizaje.pack()

    Nombre_text = tk.Label(Ventana_Aprendizaje, text = 'Nombre')
    Nombre_text.pack()
    Nombre_entry = tk.Entry(Ventana_Aprendizaje )
    Nombre_entry.pack()
    HP_text = tk.Label(Ventana_Aprendizaje, text = 'HP')
    HP_text.pack()
    HP_entry = tk.Entry(Ventana_Aprendizaje)
    HP_entry.pack()
    Marca_text = tk.Label(Ventana_Aprendizaje, text = 'Marca')
    Marca_text.pack()
    Marca_entry = tk.Entry(Ventana_Aprendizaje)
    Marca_entry.pack()
    Tipo_text = tk.Label(Ventana_Aprendizaje, text = 'Tipo')
    Tipo_text.pack()
    Tipo_entry = tk.Entry(Ventana_Aprendizaje)
    Tipo_entry.pack()
    Traccion_text = tk.Label(Ventana_Aprendizaje, text = 'Traccion')
    Traccion_text.pack()
    Traccion_entry = tk.Entry(Ventana_Aprendizaje)
    Traccion_entry.pack()
    Motor_text = tk.Label(Ventana_Aprendizaje, text = 'Motor L')
    Motor_text.pack()
    Motor_entry = tk.Entry(Ventana_Aprendizaje)
    Motor_entry.pack()
    Pistones_text = tk.Label(Ventana_Aprendizaje, text = 'Pistones')
    Pistones_text.pack()
    Pistones_entry = tk.Entry(Ventana_Aprendizaje)
    Pistones_entry.pack()
    Rin_text = tk.Label(Ventana_Aprendizaje, text = 'Rin')
    Rin_text.pack()
    Rin_entry = tk.Entry(Ventana_Aprendizaje)
    Rin_entry.pack()
    Combustible_text = tk.Label(Ventana_Aprendizaje, text = 'Combustible')
    Combustible_text.pack()
    Combustible_entry = tk.Entry(Ventana_Aprendizaje)
    Combustible_entry.pack()
    
    
    def Registrar():
        Nombre_N = Nombre_entry.get()
        print(f"El nombre es: {Nombre_N}")
        HP_N = HP_entry.get()
        print(f"El nombre es: {HP_N}")
        Marca_N = Marca_entry.get()
        print(f"El nombre es: {Marca_N}")
        Tipo_N = Tipo_entry.get()
        print(f"El nombre es: {Tipo_N}")
        Traccion_N = Traccion_entry.get()
        print(f"El nombre es: {Traccion_N}")
        Motor_N = Motor_entry.get()
        print(f"El nombre es: {Motor_N}")
        Pistones_N = Pistones_entry.get()
        print(f"El nombre es: {Pistones_N}")
        Rin_N = Rin_entry.get()
        print(f"El nombre es: {Rin_N}")
        Combustible_N = Combustible_entry.get()
        print(f"El nombre es: {Combustible_N}")
        cursor.execute("""INSERT INTO carros 
        (Nombre, Hp, Marca, Tipo, Traccion, `Motor L`, pistones, rin, `Tipo de combustible`) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (Nombre_N, HP_N, Marca_N, Tipo_N, Traccion_N, Motor_N, Pistones_N, Rin_N, Combustible_N))
        conexion.commit()
        jugar_otra_vez = messagebox.askyesno('Nuevo vehiculo guardado','¿Quieres jugar otra vez?')
        if jugar_otra_vez:
            Ventana_Aprendizaje.destroy()
            reiniciar_juego()
        else:
            Ventana_Aprendizaje.destroy()
            ventana.destroy()
                
    
    btn_registrar = tk.Button(Ventana_Aprendizaje, text="Registrar", command=Registrar, font=("Arial", 12), bg="yellow", fg="white")
    btn_registrar.pack(side=tk.BOTTOM, padx=20, pady=20)


# Elementos de la interfaz gráfica
pregunta_label = tk.Label(ventana, textvariable=pregunta_var, wraplength=400, font=("Arial", 14))
pregunta_label.pack(pady=20)

btn_si = tk.Button(ventana, text="Sí", command=responder_si, font=("Arial", 12), bg="green", fg="white")
btn_si.pack(side=tk.LEFT, padx=20, pady=20)

btn_no = tk.Button(ventana, text="No", command=responder_no, font=("Arial", 12), bg="red", fg="white")
btn_no.pack(side=tk.RIGHT, padx=20, pady=20)

# Iniciar el juego
realizar_pregunta()

ventana.mainloop()

# Cerrar conexión al cerrar la ventana
cursor.close()
conexion.close()
