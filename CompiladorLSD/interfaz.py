import tkinter as tk
from tkinter import filedialog, messagebox, Text, END
import os
import compilador
import play
import generarCodigoObjeto
import threading 

# Variables globales
run_code_ejecutado = False
codigo_generado = False
musica_ready = False
melody_player = None
melody_thread = None 
contenido_guardado = ""

# BOTONES FRAME IZQUIERDO

def limpiar_resultados_y_errores():
    resultados.delete(1.0, END)
    errores.delete(1.0, END)

def examinar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if archivo:
        with open(archivo, 'r') as file:
            texto.delete(1.0, tk.END)
            texto.insert(tk.END, file.read())

def guardar_contenido():
    global run_code_ejecutado
    global contenido_guardado
    contenido_guardado = texto.get(1.0, tk.END)
    messagebox.showinfo("Guardar", "Contenido guardado correctamente.")
    limpiar_resultados_y_errores()
    run_code_ejecutado = False

def run_code():
    global run_code_ejecutado
    global codigo_generado
    run_code_ejecutado = True
    limpiar_resultados_y_errores()
    if contenido_guardado:
        if compilador.analizar_entrada(contenido_guardado):
            errores.insert(tk.END, "COMPILACION EXITOSA\n")
            errores.insert(tk.END, "YA PUEDE GENERAR EL CODIGO OBJETO\n")
            errores.config(foreground="green")
            codigo_generado = True
        else:
            with open("ListaErrores.txt", "r") as f:
                listaErrores = f.read()
                errores.insert(tk.END, listaErrores)
                errores.config(foreground="red")
                codigo_generado = False
    else:
        messagebox.showwarning("Advertencia", "No hay contenido para analizar.")


#BOTONES FRAME DERECHO

def analizar_lexico():
    resultados.delete(1.0, END)
    if run_code_ejecutado:
        try:
            with open("SalidaLexica.txt", "r") as f:
                SalidaLexica = f.read()
                resultados.insert(tk.END, SalidaLexica)
        except Exception as e:
            errores.insert(tk.END, f"Error al leer el archivo SalidaLexica: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "Debes compilar primero.")
    
def analizar_sintactico():
    resultados.delete(1.0, END)
    if run_code_ejecutado:
        try:
            with open("SalidaSintactica.txt", "r") as f:
                SalidaSintactica = f.read()
                resultados.insert(tk.END, SalidaSintactica)
        except Exception as e:
            resultados.insert(tk.END, f"Error al leer el archivo SalidaSintactica: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "Debes compilar primero.")

def analizar_semantico():
    resultados.delete(1.0, END)
    if run_code_ejecutado:
        try:
            with open("SalidaSemantica.txt", "r") as f:
                SalidaSemantica = f.read()
                resultados.insert(tk.END, SalidaSemantica)
        except Exception as e:
            resultados.insert(tk.END, f"Error al leer el archivo SalidaSemantica: {str(e)}")
    else:
        messagebox.showwarning("Advertencia", "Debes compilar primero.")

def mostrar_codigo():
    global musica_ready
    resultados.delete(1.0, END)
    if run_code_ejecutado:
        if codigo_generado:
            generarCodigoObjeto.generar_codigo(contenido_guardado)
            try:
                with open("codigoGenerado.txt", "r") as f:
                    codigoGenerado = f.read()
                    resultados.insert(tk.END, codigoGenerado)
                    musica_ready = True
            except Exception as e:
                resultados.insert(tk.END, f"Error al leer el archivo codigoGenerado: {str(e)}")
        else:
            messagebox.showwarning("Advertencia", "Error en Compilacion")
    else:
        messagebox.showwarning("Advertencia", "Debes compilar primero.")

def play_music():
    global melody_thread
    if run_code_ejecutado:
        if musica_ready:
            melody_thread = threading.Thread(target=play_music_thread)
            melody_thread.start()
        else:
            messagebox.showwarning("Advertencia", "Primero Genere el Codigo")
    else:
        messagebox.showwarning("Advertencia", "Debes Compilar Primero")

def play_music_thread():
    global melody_player
    codigo_generado_path = 'codigoGenerado.txt' #GUARDAMOS LA RUTA
    if os.path.exists(codigo_generado_path):
        with open(codigo_generado_path, 'r') as f:
            codigo_guardado = f.read().strip()  # LEEMOS Y ELIMINAMOS ESPACIOS EN BLANC
    else:
        codigo_guardado = None
    
    if codigo_guardado:
        melody_player = play.reproducir_musica(codigo_guardado)
    else:
        messagebox.showwarning("Advertencia", "No hay contenido para reproducir.")

def stop_music():
    global melody_player
    if melody_player:
        melody_player.stop()
        messagebox.showinfo("Detener", "Reproducción de música detenida.")
    else:
        messagebox.showwarning("Advertencia", "No hay música reproduciéndose actualmente.")


##################################################################################
##########                     INTERFAZ                            ###############

root = tk.Tk()
root.title("Interfaz de Análisis")
root.geometry("1200x700")

# FRAMES

frame_izquierdo = tk.Frame(root, width=500, height=600)
frame_derecho = tk.Frame(root, width=500, height=600)

frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
frame_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# WIDGETS DEL FRAME IZQUIERDO

label_entrada = tk.Label(frame_izquierdo, text="Entrada:")
label_entrada.pack(pady=5)

frame_botones_izquierda = tk.Frame(frame_izquierdo)
frame_botones_izquierda.pack(pady=5)

boton_examinar = tk.Button(frame_botones_izquierda, text="Examinar", command=examinar_archivo)
boton_examinar.pack(side=tk.LEFT, padx=5)

boton_guardar = tk.Button(frame_botones_izquierda, text="Guardar", command=guardar_contenido)
boton_guardar.pack(side=tk.LEFT, padx=5)

boton_run = tk.Button(frame_botones_izquierda, text="Compilar", command=run_code, background="green")
boton_run.pack(side=tk.LEFT, padx=5)

texto = tk.Text(frame_izquierdo, wrap=tk.WORD)
texto.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

label_errores = tk.Label(frame_izquierdo, text="Errores:")
label_errores.pack(pady=5)

errores = tk.Text(frame_izquierdo, wrap=tk.WORD, bg="lightgray")
errores.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# WIDGETS DEL FRAME DERECHO

frame_botones_derecha = tk.Frame(frame_derecho)
frame_botones_derecha.pack(pady=5)

boton_lexico = tk.Button(frame_botones_derecha, text="Léxico", command=analizar_lexico)
boton_lexico.pack(side=tk.LEFT, padx=5)

boton_sintactico = tk.Button(frame_botones_derecha, text="Sintáctico", command=analizar_sintactico)
boton_sintactico.pack(side=tk.LEFT, padx=5)

boton_semantico = tk.Button(frame_botones_derecha, text="Semántico", command=analizar_semantico)
boton_semantico.pack(side=tk.LEFT, padx=5)

boton_codigo = tk.Button(frame_botones_derecha, text="Código", command=mostrar_codigo)
boton_codigo.pack(side=tk.LEFT, padx=5)

boton_play = tk.Button(frame_botones_derecha, text="Play", command=play_music, background="orange")
boton_play.pack(side=tk.LEFT, padx=5)

boton_stop = tk.Button(frame_botones_derecha, text="Stop", command=stop_music, background="red")
boton_stop.pack(side=tk.LEFT, padx=5)

resultados = tk.Text(frame_derecho, wrap=tk.WORD)
resultados.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)



root.mainloop()
