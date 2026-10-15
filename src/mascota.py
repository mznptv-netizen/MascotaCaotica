import tkinter as tk
from tkinter import Toplevel, messagebox
import pyautogui
import random
import os
import sys
import time
import base64
from PIL import Image, ImageTk
from pynput import keyboard

def obtener_ruta_recurso(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath("."), ruta_relativa)

# --- CONFIGURACIÓN DE LA SUPERMASCOTA GIGANTE ---
ANCHO_MASCOTA = 400
ALTO_MASCOTA = 400
VELOCIDAD = 8
INTERVALO_ROBO_SEGUNDOS = 10

# CONTRASEÑA OCULTA (El texto "NDI1NA==" corresponde a "4254" en Base64)
# Nadie podrá adivinar la clave solo leyendo tu repositorio de GitHub.
CLAVE_OCULTA_B64 = "NDI1NA=="

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
        self.bloqueo_activo = False

        # ACTIVAR BLOQUEO DE TECLADO FÍSICO EN SEGUNDO PLANO
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
            self.delay_mascota = max(20, im.info.get('duration', 100))
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
        for _ in range(15):
            pyautogui.moveTo(random.randint(50, sw - 50), random.randint(50, sh - 50), duration=0.03)

    def pedir_contrasena_virtual_mejorada(self):
        """Abre un teclado numérico digital GIGANTE que CAPTURA TODO EL INPUT DEL MOUSE"""
        if self.bloqueo_activo: return
        self.bloqueo_activo = True

        v_tec = Toplevel(self.window)
        v_tec.title("¡BLOQUEO TOTAL - INGRESA LA CLAVE SECRETA!")
        v_tec.wm_attributes("-topmost", True)
        v_tec.config(bg="#1a1a1a")
        v_tec.geometry("400x600")

        v_tec.grab_set() 

        def al_cerrar_forzado():
            self.bloqueo_activo = False
            v_tec.destroy()
            self.activar_castigo_masivo()

        v_tec.protocol("WM_DELETE_WINDOW", al_cerrar_forzado)

        txt_var = tk.StringVar()
        lbl_pantalla = tk.Label(v_tec, textvariable=txt_var, font=("Arial", 32, "bold"), bg="black", fg="#00FF00", width=10, relief="sunken")
        lbl_pantalla.pack(pady=25)

        pass_ingresada = {"val": ""}

        def presionar_tecla(digito):
            if len(pass_ingresada["val"]) < 6:
                pass_ingresada["val"] += str(digito)
                txt_var.set("*" * len(pass_ingresada["val"]))

        def borrar():
            pass_ingresada["val"] = ""
            txt_var.set("")

        def enviar():
            # Codificamos lo que escribió el usuario a Base64 para compararlo de forma oculta
            usuario_b64 = base64.b64encode(pass_ingresada["val"].encode('utf-8')).decode('utf-8')

            if usuario_b64 == CLAVE_OCULTA_B64:
                self.bloqueo_activo = False
                v_tec.grab_release()
                messagebox.showinfo("¡Liberado!", "Contraseña correcta. Tienes 10 segundos.")
                v_tec.destroy()
            else:
                messagebox.showerror("¡Error!", "¡Contraseña incorrecta!")
                borrar()
                self.activar_castigo_masivo()

        frame_botones = tk.Frame(v_tec, bg="#1a1a1a")
        frame_botones.pack(pady=10)

        botones = [
            ('1', 0, 0), ('2', 0, 1), ('3', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2),
            ('C', 3, 0), ('0', 3, 1), ('OK', 3, 2)
        ]

        for (texto, r, c) in botones:
            if texto == 'C':
                cmd, bg_color, fg_color = borrar, "#d9534f", "white"
            elif texto == 'OK':
                cmd, bg_color, fg_color = enviar, "#5cb85c", "white"
            else:
                cmd, bg_color, fg_color = lambda t=texto: presionar_tecla(t), "#f0f0f0", "black"

            btn = tk.Button(frame_botones, text=texto, font=("Arial", 20, "bold"), width=6, height=3, command=cmd, bg=bg_color, fg=fg_color, relief="raised")
            btn.grid(row=r, column=c, padx=10, pady=10)

    def activar_castigo_masivo(self):
        for _ in range(4):
            if os.path.exists(IMAGEN_ROBO):
                self.mostrar_ventana_multimedia(IMAGEN_ROBO, "¡CASTIGO TOTAL!", es_imagen_robo=True)

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

            self.window.after(100, self.pedir_contrasena_virtual_mejorada)

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
                self.mostrar_ventana_multimedia(IMAGEN_ROBO, "¡MULTIPLICACIÓN HIDRA!", es_imagen_robo=True)
                self.mostrar_ventana_multimedia(IMAGEN_ROBO, "¡NO PUEDES ESCAPAR!", es_imagen_robo=True)
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
