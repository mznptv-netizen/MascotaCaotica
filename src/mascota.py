import tkinter as tk
from tkinter import Toplevel, messagebox
import pyautogui
import random
import os
import sys
import time
from PIL import Image, ImageTk
from pynput import keyboard

def obtener_ruta_recurso(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath("."), ruta_relativa)

# --- CONFIGURACIÓN ---
ANCHO_MASCOTA = 250
ALTO_MASCOTA = 250
VELOCIDAD = 7
INTERVALO_ROBO_SEGUNDOS = 10
CLASE_CLAVE_SECRETA = "4254"  # ¡Contraseña exacta requerida!

CARPETA_RANDOM = obtener_ruta_recurso("imagenes_random")
IMAGEN_MASCOTA = obtener_ruta_recurso("mascota.png")
IMAGEN_ROBO = obtener_ruta_recurso("imagen_robo.png")

class MascotaCaotica:
    def __init__(self):
        self.window = tk.Tk()

        # Configurar ventana transparente y siempre arriba
        self.window.overrideredirect(True)
        self.window.wm_attributes("-topmost", True)
        self.window.config(bg='magenta')
        self.window.wm_attributes("-transparentcolor", "magenta")

        if not os.path.exists(IMAGEN_MASCOTA):
            print(f"Error: No se encontró '{IMAGEN_MASCOTA}'")
            self.window.destroy()
            return

        self.label = tk.Label(self.window, bg='magenta')
        self.label.pack()
        
        self.frames_mascota = []
        self.delay_mascota = 100
        self.cargar_animacion_principal(IMAGEN_MASCOTA)
        self.frame_actual_idx = 0

        self.x, self.y = 500, 500
        self.window.geometry(f"+{self.x}+{self.y}")

        self.lista_random = self._cargar_imagenes_random()
        self.ultimo_robo = time.time()
        self.teclado_abierto = False  # Evita que se abran múltiples teclados a la vez

        # ACTIVAR BLOQUEO DE TECLADO EN SEGUNDO PLANO
        self.iniciar_bloqueo_teclado()

        self.animar_mascota()
        self.window.after(100, self.actualizar)
        self.window.mainloop()

    def iniciar_bloqueo_teclado(self):
        """Bloquea cualquier tecla física que se intente presionar"""
        def on_press(key):
            return False

        self.listener_teclado = keyboard.Listener(on_press=on_press)
        self.listener_teclado.daemon = True
        self.listener_teclado.start()

    def cargar_animacion_principal(self, ruta):
        try:
            im = Image.open(ruta)
            self.delay_mascota = im.info.get('duration', 100)
            if self.delay_mascota < 20: self.delay_mascota = 100
            for frame in range(im.n_frames):
                im.seek(frame)
                temp_img = im.copy().resize((ANCHO_MASCOTA, ALTO_MASCOTA))
                self.frames_mascota.append(ImageTk.PhotoImage(temp_img))
        except Exception:
            im = Image.open(ruta).resize((ANCHO_MASCOTA, ALTO_MASCOTA))
            self.frames_mascota.append(ImageTk.PhotoImage(im))

    def animar_mascota(self):
        if self.frames_mascota:
            self.frame_actual_idx = (self.frame_actual_idx + 1) % len(self.frames_mascota)
            self.label.configure(image=self.frames_mascota[self.frame_actual_idx])
            self.window.after(self.delay_mascota, self.animar_mascota)

    def _cargar_imagenes_random(self):
        if not os.path.exists(CARPETA_RANDOM): return []
        return [os.path.join(CARPETA_RANDOM, f) for f in os.listdir(CARPETA_RANDOM) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    def mover_mouse_agresivo(self):
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        for _ in range(12):
            pyautogui.moveTo(random.randint(50, sw - 50), random.randint(50, sh - 50), duration=0.04)

    def pedir_contrasena_con_teclado_virtual(self):
        """Abre una ventana con un teclado numérico digital interactuable solo con el mouse"""
        if self.teclado_abierto:
            return
        self.teclado_abierto = True

        v_tec = Toplevel(self.window)
        v_tec.title("¡TECLADO BLOQUEADO - INGRESA CONTRASEÑA 4254!")
        v_tec.wm_attributes("-topmost", True)
        v_tec.config(bg="#222222")
        v_tec.geometry("320+400+300")

        # Evitar que cierren la ventana de la X sin castigo
        def al_cerrar_forzado():
            self.teclado_abierto = False
            v_tec.destroy()
            self.activar_castigo_masivo()

        v_tec.protocol("WM_DELETE_WINDOW", al_cerrar_forzado)

        # Pantalla de texto donde se ve la contraseña oculta con asteriscos
        txt_var = tk.StringVar()
        lbl_pantalla = tk.Label(v_tec, textvariable=txt_var, font=("Arial", 22, "bold"), bg="black", fg="#00FF00", width=12, relief="sunken")
        lbl_pantalla.pack(pady=15)

        pass_ingresada = {"val": ""}

        def presionar_tecla(digito):
            if len(pass_ingresada["val"]) < 8:
                pass_ingresada["val"] += str(digito)
                txt_var.set("*" * len(pass_ingresada["val"]))

        def borrar():
            pass_ingresada["val"] = ""
            txt_var.set("")

        def enviar():
            if pass_ingresada["val"] == CLASE_CLAVE_SECRETA:
                self.teclado_abierto = False
                messagebox.showinfo("¡Acceso concedido!", "Contraseña correcta. Tienes 10 segundos de paz.")
                v_tec.destroy()
            else:
                messagebox.showerror("¡Error!", "¡Contraseña incorrecta!")
                borrar()
                self.activar_castigo_masivo()

        # Cuadrícula de botones numéricos (Diseño solo mouse)
        frame_botones = tk.Frame(v_tec, bg="#222222")
        frame_botones.pack(pady=5)

        botones = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('C', 3, 0), ('0', 3, 1), ('OK', 3, 2)
        ]

        for (texto, r, c) in botones:
            if texto == 'C':
                cmd = borrar
                bg_color = "#D9534F"
            elif texto == 'OK':
                cmd = enviar
                bg_color = "#5CB85C"
            else:
                cmd = lambda t=texto: presionar_tecla(t)
                bg_color = "#F0F0F0"

            btn = tk.Button(frame_botones, text=texto, font=("Arial", 16, "bold"), width=5, height=2, command=cmd, bg=bg_color)
            btn.grid(row=r, column=c, padx=5, pady=5)

    def activar_castigo_masivo(self):
        """Lanza múltiples imágenes de robo como castigo"""
        for _ in range(3):
            if os.path.exists(IMAGEN_ROBO):
                self.mostrar_ventana_multimedia(IMAGEN_ROBO, "¡CASTIGO POR FALLAR!", es_imagen_robo=True)

    def actualizar(self):
        mx, my = pyautogui.position()
        target_x, target_y = mx - (ANCHO_MASCOTA // 2), my - (ALTO_MASCOTA // 2)

        if self.x < target_x: self.x += VELOCIDAD
        elif self.x > target_x: self.x -= VELOCIDAD
        if self.y < target_y: self.y += VELOCIDAD
        elif self.y > target_y: self.y -= VELOCIDAD

        self.window.geometry(f"+{self.x}+{self.y}")

        tiempo_actual = time.time()
        if tiempo_actual - self.ultimo_robo >= INTERVALO_ROBO_SEGUNDOS:
            self.ultimo_robo = tiempo_actual
            self.mover_mouse_agresivo()

            # Abrir el teclado numérico en pantalla
            self.pedir_contrasena_con_teclado_virtual()

            # Mostrar imagen de robo inicial y meme aleatorio
            if os.path.exists(IMAGEN_ROBO):
                self.mostrar_ventana_multimedia(IMAGEN_ROBO, "¡TE ROBÉ EL MOUSE!", es_imagen_robo=True)

            if self.lista_random:
                self.mostrar_ventana_multimedia(random.choice(self.lista_random), "Meme Random Caótico", es_imagen_robo=False)

        self.window.after(20, self.actualizar)

    def mostrar_ventana_multimedia(self, ruta_img, titulo="", es_imagen_robo=False):
        v = Toplevel(self.window)
        v.title(titulo)
        v.wm_attributes("-topmost", True)

        if es_imagen_robo:
            def al_cerrar():
                v.destroy()
                self.mostrar_ventana_multimedia(IMAGEN_ROBO, "¡MULTIPLICACIÓN!", es_imagen_robo=True)
                self.mostrar_ventana_multimedia(IMAGEN_ROBO, "¡NO TE VAS A SALVAR!", es_imagen_robo=True)
            v.protocol("WM_DELETE_WINDOW", al_cerrar)

        lbl = tk.Label(v)
        lbl.pack()

        frames, delay = [], 100
        try:
            im = Image.open(ruta_img)
            delay = max(20, im.info.get('duration', 100))
            for frame in range(im.n_frames):
                im.seek(frame)
                temp = im.copy()
                temp.thumbnail((350, 350))
                frames.append(ImageTk.PhotoImage(temp))
        except Exception:
            im = Image.open(ruta_img)
            im.thumbnail((350, 350))
            frames.append(ImageTk.PhotoImage(im))

        def animar(idx=0):
            if v.winfo_exists() and frames:
                lbl.configure(image=frames[idx])
                v.frames_ref = frames
                v.after(delay, lambda: animar((idx + 1) % len(frames)))

        animar()
        sw, sh = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        v.geometry(f"+{random.randint(50, sw-400)}+{random.randint(50, sh-400)}")

if __name__ == "__main__":
    MascotaCaotica()
