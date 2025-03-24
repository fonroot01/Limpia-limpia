# Hola, este script fue desarrollado en python por Alfonso Mosquera
# Cualquier novedad o asistencia te puedes comunicar conmigo por correo: alfomosque22@gmail.com

import os
import shutil
import time
import psutil
import tkinter as tk
from tkinter import scrolledtext

def cerrar_procesos():
    """ Cierra navegadores antes de limpiar historial """
    procesos = ["chrome.exe", "msedge.exe"]
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if proc.info["name"].lower() in procesos:
                psutil.Process(proc.info["pid"]).terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

def eliminar_archivos_temporales(log_text):
    rutas = [
        os.getenv("TEMP"),
        os.getenv("TMP"),
        os.path.expanduser(r"~\AppData\Local\Temp"),
        os.path.expanduser(r"C:\Windows\Temp")
    ]

    for ruta in rutas:
        if ruta and os.path.exists(ruta):
            for archivo in os.listdir(ruta):
                archivo_path = os.path.join(ruta, archivo)
                try:
                    if os.path.isfile(archivo_path) or os.path.islink(archivo_path):
                        os.unlink(archivo_path)
                        log_text.insert(tk.END, f"Eliminado: {archivo_path}\n")
                    elif os.path.isdir(archivo_path):
                        shutil.rmtree(archivo_path, ignore_errors=True)
                        log_text.insert(tk.END, f"Carpeta eliminada: {archivo_path}\n")
                except PermissionError:
                    log_text.insert(tk.END, f"❌ Archivo en uso: {archivo_path}\n")
                except Exception as e:
                    log_text.insert(tk.END, f"⚠️ Error en {archivo_path}: {e}\n")

def eliminar_historial_navegador(log_text):
    cerrar_procesos()  # Asegura que los navegadores estén cerrados

    rutas_historial = [
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data\Default\History"),
        os.path.expanduser(r"~\AppData\Local\Microsoft\Edge\User Data\Default\History")
    ]

    for ruta in rutas_historial:
        if os.path.exists(ruta):
            try:
                os.remove(ruta)
                log_text.insert(tk.END, f"✔ Historial eliminado: {ruta}\n")
            except PermissionError:
                log_text.insert(tk.END, f"❌ No se pudo eliminar {ruta}, intenta nuevamente.\n")
            except Exception as e:
                log_text.insert(tk.END, f"⚠️ Error eliminando historial en {ruta}: {e}\n")

def vaciar_papelera(log_text):
    try:
        os.system("powershell.exe -Command Clear-RecycleBin -Confirm:$false")
        log_text.insert(tk.END, "✔ Papelera vaciada.\n")
    except Exception as e:
        log_text.insert(tk.END, f"⚠️ Error al vaciar la papelera: {e}\n")

def main():
    root = tk.Tk()
    root.title("Limpia limpia")
    root.geometry("600x400")
    root.iconbitmap(r"C:\Users\Alfonso\OneDrive\Escritorio\Auditorias\1 SCRIPTS PYTHON ORIENTADO A LA C-SEGURIDAD\Limpia limpia\Limpia_limpiaicono.ico")

    log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=15)
    log_text.pack(pady=10)

    tk.Button(root, text="Limpiar Archivos Temporales", command=lambda: eliminar_archivos_temporales(log_text)).pack(pady=5)
    tk.Button(root, text="Limpiar Historial Navegador", command=lambda: eliminar_historial_navegador(log_text)).pack(pady=5)
    tk.Button(root, text="Vaciar Papelera", command=lambda: vaciar_papelera(log_text)).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

