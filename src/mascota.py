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

# --- CONFIGURACIÓN DE LA SUPERMASCOTA AGRESIVA ---
ANCHO_MASCOTA = 250  # ¡Mucho más grande!
ALTO_MASCOTA = 250
VELOCIDAD = 7         # Más rápida
INTERVALO_ROBO_SEGUNDOS = 10

CARPETA_RANDOM = obtener_ruta_recurso("imagenes_random")
IMAGEN_MASCOTA = obtener_ruta_recurso("mascota.png")
IMAGEN_ROBO = obtener_ruta_recurso("imagen_robo.png")

class MascotaCaotica:
    def __init__(self):
        self.window = tk.Tk()

        # Configurar ventana transparente y siempre arriba de todo
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)
        self.window.config(bg='magenta')
        self.window.wm_attributes("-transparentcolor", "magenta")

        if not os.path.exists(IMAGEN_MASCOTA):
            print(f"Error: No se encontró '{IMAGEN_MASCOTA}'")
            self.window.destroy()
            return

        # Configurar etiqueta principal
        self.label = tk.Label(self.window, bg='magenta')
        self.label.pack()
        
        self.frames_mascota = []
        self.delay_mascota = 100
        self.cargar_animacion_principal(IMAGEN_MASCOTA)
        self.frame_actual_idx = 0

        # Posición inicial
        self.x, self.y = 500, 500
        self.window.geometry(f"+{self.x}+{self.y}")

        # Cargar imágenes de la carpeta aleatoria
        self.lista_random = self._cargar_imagenes_random()

        # Temporizador para el robo del mouse
        self.ultimo_robo = time.time()

        # Iniciar animaciones y bucle
        self.animar_mascota()
        self.window.after(100, self.actualizar)
        self.window.mainloop()

    def cargar_animacion_principal(self, ruta):
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
        if self.frames_mascota:
            self.frame_actual_idx = (self.frame_actual_idx + 1) % len(self.frames_mascota)
            self.label.configure(image=self.frames_mascota[self.frame_actual_idx])
            self.window.after(self.delay_mascota, self.animar_mascota)

    def _cargar_imagenes_random(self):
        if not os.path.exists(CARPETA_RANDOM):
            return []
        archivos = os.listdir(CARPETA_RANDOM)
        return [os.path.join(CARPETA_RANDOM, f) for f in archivos if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    def mover_mouse_agresivo(self):
        """Mueve el cursor frenéticamente por toda la pantalla"""
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        # Sacude el mouse en 10 puntos aleatorios muy rápido
        for _ in range(12):
            rx = random.randint(50, sw - 50)
            ry = random.randint(50, sh - 50)
            pyautogui.moveTo(rx, ry, duration=0.04)

    def actualizar(self):
        # 1. Movimiento constante de persecución agresiva hacia el mouse
        mx, my = pyautogui.position()
        target_x = mx - (ANCHO_MASCOTA // 2)
        target_y = my - (ALTO_MASCOTA // 2)

        if self.x < target_x: self.x += VELOCIDAD
        elif self.x > target_x: self.x -= VELOCIDAD

        if self.y < target_y: self.y += VELOCIDAD
        elif self.y > target_y: self.y -= VELOCIDAD

        self.window.geometry(f"+{self.x}+{self.y}")

        # 2. Comprobar si pasaron los 10 segundos para el ATAQUE AGRESIVO
        tiempo_actual = time.time()
        if tiempo_actual - self.ultimo_robo >= INTERVALO_ROBO_SEGUNDOS:
            self.ultimo_robo = tiempo_actual

            # ATAQUE 1: Mover el mouse descontroladamente por toda la pantalla
            self.mover_mouse_agresivo()

            # ATAQUE 2: Abrir la imagen de robo con el "Efecto Hidra" (Cierras 1, se abren 2)
            if os.path.exists(IMAGEN_ROBO):
                self.mostrar_ventana_multimedia(IMAGEN_ROBO, "¡TE ROBÉ EL MOUSE!", es_imagen_robo=True)

            # ATAQUE 3: Abrir meme aleatorio de la carpeta
            if self.lista_random:
                img_path = random.choice(self.lista_random)
                self.mostrar_ventana_multimedia(img_path, "Meme Random Caótico", es_imagen_robo=False)

        self.window.after(20, self.actualizar)

    def mostrar_ventana_multimedia(self, ruta_img, titulo="", es_imagen_robo=False):
        """Crea ventanas emergentes y aplica el efecto de multiplicar por 2 al cerrar si es la imagen de robo."""
        v = Toplevel(self.window)
        v.title(titulo)
        v.wm_attributes("-topmost", True)

        # Lógica del Efecto Hidra: Si se cierra la imagen de robo, abre 2 nuevas
        if es_imagen_robo:
            def al_cerrar():
                v.destroy()
                # Se abren 2 ventanas más de robo
                self.mostrar_ventana_multimedia(IMAGEN_ROBO, "¡NO PUEDES CERRARME!", es_imagen_robo=True)
                self.mostrar_ventana_multimedia(IMAGEN_ROBO, "¡AHORA SOMOS DOS!", es_imagen_robo=True)

            v.protocol("WM_DELETE_WINDOW", al_cerrar)

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
