import tkinter as tk
from tkinter import Toplevel
import pyautogui
import random
import os
import sys
import time
from PIL import Image, ImageTk

def obtener_ruta_recurso(ruta_relativa):
    """ Obtiene la ruta absoluta de recursos para ejecutable o desarrollo """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath("."), ruta_relativa)

# --- CONFIGURACIÓN ---
ANCHO_MASCOTA = 100
ALTO_MASCOTA = 100
VELOCIDAD = 4
INTERVALO_ROBO_SEGUNDOS = 10 # El mouse se roba exactamente cada 10 segundos

CARPETA_RANDOM = obtener_ruta_recurso("imagenes_random")
IMAGEN_MASCOTA = obtener_ruta_recurso("mascota.png") # Puede ser .png o .gif (la mascota principal)
IMAGEN_ROBO = obtener_ruta_recurso("imagen_robo.png") # Imagen o GIF específico al robar el mouse

class MascotaCaotica:
    def __init__(self):
        self.window = tk.Tk()

        # Configurar ventana transparente y siempre encima
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)
        self.window.config(bg='magenta')
        self.window.wm_attributes("-transparentcolor", "magenta")

        if not os.path.exists(IMAGEN_MASCOTA):
            print(f"Error: No se encontró '{IMAGEN_MASCOTA}'")
            self.window.destroy()
            return

        # Configurar etiqueta principal (Soporta GIFs animados)
        self.label = tk.Label(self.window, bg='magenta')
        self.label.pack()
        
        self.frames_mascota = []
        self.delay_mascota = 100
        self.cargar_animacion_principal(IMAGEN_MASCOTA)
        self.frame_actual_idx = 0

        # Posición inicial
        self.x, self.y = 500, 500
        self.window.geometry(f"+{self.x}+{self.y}")

        # Cargar imágenes de la carpeta aleatoria (opcional)
        self.lista_random = self._cargar_imagenes_random()

        # Temporizador para el robo del mouse cada 10 segundos
        self.ultimo_robo = time.time()

        # Iniciar animaciones y bucle
        self.animar_mascota()
        self.window.after(100, self.actualizar)
        self.window.mainloop()

    def cargar_animacion_principal(self, ruta):
        """Carga frames si es GIF o imagen estática para la mascota."""
        try:
            im = Image.open(ruta)
            self.delay_mascota = im.info.get('duration', 100)
            if self.delay_mascota < 20: 
                self.delay_mascota = 100
            
            for frame in range(im.n_frames):
                im.seek(frame)
                temp_img = im.copy().resize((ANCHO_MASCOTA, ALTO_MASCOTA))
                self.frames_mascota.append(ImageTk.PhotoImage(temp_img))
        except EOFError:
            pass
        except Exception:
            im = Image.open(ruta).resize((ANCHO_MASCOTA, ALTO_MASCOTA))
            self.frames_mascota.append(ImageTk.PhotoImage(im))

    def animar_mascota(self):
        """Bucle para reproducir la animación GIF de la mascota."""
        if self.frames_mascota:
            self.frame_actual_idx = (self.frame_actual_idx + 1) % len(self.frames_mascota)
            self.label.configure(image=self.frames_mascota[self.frame_actual_idx])
            self.window.after(self.delay_mascota, self.animar_mascota)

    def _cargar_imagenes_random(self):
        if not os.path.exists(CARPETA_RANDOM):
            return []
        archivos = os.listdir(CARPETA_RANDOM)
        return [os.path.join(CARPETA_RANDOM, f) for f in archivos if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    def actualizar(self):
        # 1. Movimiento constante de persecución hacia el mouse
        mx, my = pyautogui.position()
        target_x = mx - (ANCHO_MASCOTA // 2)
        target_y = my - (ALTO_MASCOTA // 2)

        if self.x < target_x: self.x += VELOCIDAD
        elif self.x > target_x: self.x -= VELOCIDAD

        if self.y < target_y: self.y += VELOCIDAD
        elif self.y > target_y: self.y -= VELOCIDAD

        self.window.geometry(f"+{self.x}+{self.y}")

        # 2. Comprobar si ya pasaron los 10 segundos para el evento de robo
        tiempo_actual = time.time()
        if tiempo_actual - self.ultimo_robo >= INTERVALO_ROBO_SEGUNDOS:
            self.ultimo_robo = tiempo_actual # Reiniciar cronómetro

            # ACCIÓN DE ROBO CADA 10 SEGUNDOS:
            pyautogui.moveTo(mx + random.randint(-250, 250), my + random.randint(-250, 250), duration=0.1)

            # Mostrar la imagen o GIF específico del robo
            if os.path.exists(IMAGEN_ROBO):
                self.mostrar_ventana_multimedia(IMAGEN_ROBO, "¡Te robé el mouse!")

        # Repetir bucle constantemente
        self.window.after(30, self.actualizar)

    def mostrar_ventana_multimedia(self, ruta_img, titulo=""):
        """Crea una ventana emergente que soporta imágenes estáticas o GIFs."""
        v = Toplevel(self.window)
        v.title(titulo)
        v.wm_attributes("-topmost", True)

        lbl_emergente = tk.Label(v)
        lbl_emergente.pack()

        frames = []
        delay = 100

        try:
            im = Image.open(ruta_img)
            delay = im.info.get('duration', 100)
            if delay < 20: delay = 100

            for frame in range(im.n_frames):
                im.seek(frame)
                temp_img = im.copy()
                temp_img.thumbnail((350, 350))
                frames.append(ImageTk.PhotoImage(temp_img))
        except EOFError:
            pass
        except Exception:
            im = Image.open(ruta_img)
            im.thumbnail((350, 350))
            frames.append(ImageTk.PhotoImage(im))

        def animar_emergente(idx=0):
            if v.winfo_exists() and frames:
                lbl_emergente.configure(image=frames[idx])
                v.frames_ref = frames 
                v.after(delay, lambda: animar_emergente((idx + 1) % len(frames)))

        animar_emergente()

        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        v.geometry(f"+{random.randint(50, sw-400)}+{random.randint(50, sh-400)}")

if __name__ == "__main__":
    MascotaCaotica()
