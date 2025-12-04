import tkinter as tk
import logging
from tkinter import ttk, messagebox
from src.estilos import *
from src.modelo import Estado

class AplicacionGUI:
    def __init__(self, root: tk.Tk, auth_manager, taxi_manager, config_manager):
        self.root = root
        self.auth = auth_manager
        self.taxi = taxi_manager
        self.config = config_manager
        
        self._configurar_ventana_principal()
        self.frame_actual = None
        
        self._mostrar_login()

    def _configurar_ventana_principal(self):
        self.root.title(TXT_TITULO_APP)
        # Ajustamos tamaño: un poco más ancho para que la tarjeta respire
        self.root.geometry("500x700") 
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_FONDO_APP)
        
        # Estilos globales TTK
        style = ttk.Style()
        style.theme_use('clam')
        # Hacemos el borde del input más sutil
        style.configure("TEntry", padding=5, relief="flat", borderwidth=1)

    def _limpiar_frame(self):
        if self.frame_actual:
            self.frame_actual.destroy()

    # ==========================================
    # 1. PANTALLA DE LOGIN (REDISEÑO "PRO")
    # ==========================================
    def _mostrar_login(self):
        self._limpiar_frame()
        
        # Frame de fondo que ocupa todo
        self.frame_actual = tk.Frame(self.root, bg=COLOR_FONDO_APP)
        self.frame_actual.pack(expand=True, fill='both')

        # === TARJETA FLOTANTE ===
        # Dimensiones ajustadas: width=360, height=440 (Más proporcionada)
        card = tk.Frame(self.frame_actual, bg="white")
        card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=440)

        # 1. Franja decorativa superior (Toque de color)
        top_stripe = tk.Frame(card, bg=COLOR_ACENTO, height=6)
        top_stripe.pack(fill='x', side='top')

        # 2. Icono y Título
        # Usamos Segoe UI Emoji para que el taxi se vea mejor, o una fuente grande
        tk.Label(card, text="🚖", font=("Segoe UI Emoji", 42), bg="white", fg=COLOR_TEXTO_MAIN).pack(pady=(30, 10))
        
        tk.Label(card, text="Bienvenido", font=("Segoe UI", 22, "bold"), 
                 bg="white", fg=COLOR_TEXTO_MAIN).pack(pady=(0, 25))

        # 3. Contenedor de Inputs (Para márgenes laterales limpios)
        input_frame = tk.Frame(card, bg="white")
        input_frame.pack(fill='both', expand=True, padx=40)

        # Usuario
        tk.Label(input_frame, text="USUARIO", font=("Segoe UI", 9, "bold"), 
                 bg="white", fg="#7f8c8d").pack(anchor='w', pady=(0, 5))
        
        self.entry_user = ttk.Entry(input_frame, font=("Segoe UI", 11))
        # ipady=4 hace la caja más alta y moderna
        self.entry_user.pack(fill='x', ipady=4, pady=(0, 20))
        self.entry_user.focus() # Poner cursor aquí automáticamente

        # Contraseña
        tk.Label(input_frame, text="CONTRASEÑA", font=("Segoe UI", 9, "bold"), 
                 bg="white", fg="#7f8c8d").pack(anchor='w', pady=(0, 5))
        
        self.entry_pass = ttk.Entry(input_frame, show="•", font=("Segoe UI", 11))
        self.entry_pass.pack(fill='x', ipady=4, pady=(0, 25))

        # 4. Botón de Acción (Full width)
        # Flat relief y cursor hand le dan toque web
        btn = tk.Button(input_frame, text=TXT_BTN_LOGIN, bg=COLOR_ACENTO, fg="white",
                        font=("Segoe UI", 11, "bold"), relief="flat", cursor="hand2",
                        activebackground="#1f618d", activeforeground="white",
                        command=self._accion_login)
        btn.pack(fill='x', ipady=8, pady=(0, 20))
        
        # 5. Footer (Versión)
        tk.Label(card, text="v2.0 Expert System", font=("Segoe UI", 8), 
                 bg="white", fg="#bdc3c7").pack(side='bottom', pady=15)
        
        # Bind Enter
        self.root.bind('<Return>', lambda e: self._accion_login())

    def _accion_login(self):
        user = self.entry_user.get()
        logging.info(f"Intento de login: '{user}'")
        
        if self.auth.login(user, self.entry_pass.get()):
            self.root.unbind('<Return>')
            self._mostrar_dashboard()
        else:
            logging.warning(f"Login fallido: '{user}'")
            messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.")

    # ==========================================
    # 2. PANTALLA DASHBOARD (Con Configuración)
    # ==========================================
    def _mostrar_dashboard(self):
        self._limpiar_frame()
        self.frame_actual = tk.Frame(self.root, bg=COLOR_FONDO_APP) # Fondo oscuro general
        self.frame_actual.pack(expand=True, fill='both')

        # Header (Barra superior)
        header = tk.Frame(self.frame_actual, bg="#34495e", height=50)
        header.pack(fill='x')
        
        # Botón Configuración (Izquierda)
        btn_conf = tk.Button(header, text="⚙️", bg="#34495e", fg="white", bd=0, 
                             font=("Segoe UI", 14), cursor="hand2",
                             command=self._mostrar_configuracion)
        btn_conf.pack(side='left', padx=10)

        # Info Usuario (Derecha)
        tk.Label(header, text=f"Hola, {self.auth.usuario_actual}", 
                 font=FONT_NORMAL, bg="#34495e", fg="white").pack(side='right', padx=15, pady=10)

        # === PANEL PRINCIPAL (Blanco redondeado visualmente) ===
        panel = tk.Frame(self.frame_actual, bg="#ecf0f1")
        panel.pack(expand=True, fill='both', pady=(0, 0)) # Ocupa el resto

        # Display Digital
        display_frame = tk.Frame(panel, bg=COLOR_DISPLAY_BG, bd=4, relief="sunken")
        display_frame.pack(fill='x', padx=20, pady=30)

        self.var_precio = tk.StringVar(value="LIBRE")
        self.var_tiempo = tk.StringVar(value="--:--")
        
        tk.Label(display_frame, textvariable=self.var_precio, font=FONT_DIGITAL, 
                 bg=COLOR_DISPLAY_BG, fg=COLOR_DISPLAY_FG).pack(pady=(15, 5))
        tk.Label(display_frame, textvariable=self.var_tiempo, font=FONT_DIGITAL_SMALL, 
                 bg=COLOR_DISPLAY_BG, fg=COLOR_DISPLAY_FG).pack(pady=(0, 15))

        # Estado Visual
        self.var_estado_txt = tk.StringVar(value="LIBRE")
        self.lbl_estado = tk.Label(panel, textvariable=self.var_estado_txt, 
                                   font=("Segoe UI", 12, "bold"), bg="#ecf0f1", fg=COLOR_TEXTO_MAIN)
        self.lbl_estado.pack(pady=5)

        # Botonera
        btn_frame = tk.Frame(panel, bg="#ecf0f1")
        btn_frame.pack(fill='both', expand=True, padx=30, pady=10)

        # Botón Marcha/Paro (Estado)
        self.btn_marcha = tk.Button(btn_frame, text="⏯ ARRANCAR / FRENAR", font=FONT_BOTON,
                                    bg=COLOR_ACENTO, fg="white", state="disabled",
                                    relief="flat", cursor="hand2",
                                    command=self._alternar_marcha)
        self.btn_marcha.pack(fill='x', pady=10, ipady=8)

        # Botón Start/Stop (Ciclo)
        self.btn_principal = tk.Button(btn_frame, text="▶ INICIAR CARRERA", font=FONT_BOTON,
                                       bg=COLOR_PRIMARIO, fg="white",
                                       relief="flat", cursor="hand2",
                                       command=self._gestion_ciclo_vida)
        self.btn_principal.pack(fill='x', pady=10, ipady=12)

        # Botón Salir
        tk.Button(panel, text="Cerrar Sesión", command=self._accion_logout,
                  bg=COLOR_SECUNDARIO, fg="white", relief="flat").pack(side='bottom', fill='x', pady=0, ipady=10)

        self._loop_actualizar_ui()

    # ==========================================
    # 3. PANTALLA DE CONFIGURACIÓN (NUEVA)
    # ==========================================
    def _mostrar_configuracion(self):
        # Evitar entrar si hay carrera (seguridad)
        if self.taxi.en_trayecto:
            messagebox.showwarning("Bloqueado", "No puedes cambiar la configuración durante una carrera.")
            return

        self._limpiar_frame()
        self.frame_actual = tk.Frame(self.root, bg=COLOR_FONDO_APP)
        self.frame_actual.pack(expand=True, fill='both')

        # Tarjeta Config
        card = tk.Frame(self.frame_actual, bg=COLOR_CARD_BG)
        card.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)

        tk.Label(card, text="⚙️ Configuración", font=FONT_TITULO_LOGIN, 
                 bg=COLOR_CARD_BG, fg=COLOR_TEXTO_MAIN).pack(pady=20)

        # Campos
        def crear_input(texto, valor_actual):
            frame = tk.Frame(card, bg=COLOR_CARD_BG)
            frame.pack(fill='x', padx=30, pady=10)
            tk.Label(frame, text=texto, font=FONT_SUBTITULO, bg=COLOR_CARD_BG, fg=COLOR_TEXTO_LIGHT).pack(anchor='w')
            entry = ttk.Entry(frame, font=FONT_NORMAL)
            entry.insert(0, str(valor_actual))
            entry.pack(fill='x', pady=5)
            return entry

        # Cargar valores actuales
        val_parado = self.config.get_tarifa("parado")
        val_mov = self.config.get_tarifa("movimiento")

        self.entry_conf_parado = crear_input(f"Tarifa Parado ({self.config.moneda}/s)", val_parado)
        self.entry_conf_mov = crear_input(f"Tarifa Movimiento ({self.config.moneda}/s)", val_mov)

        # Botones Acción
        btn_save = tk.Button(card, text=TXT_BTN_GUARDAR, bg=COLOR_PRIMARIO, fg="white",
                             font=FONT_BOTON, relief="flat", command=self._guardar_configuracion)
        btn_save.pack(fill='x', padx=30, pady=(30, 10), ipady=5)

        btn_back = tk.Button(card, text=TXT_BTN_VOLVER, bg=COLOR_NEUTRO, fg="white",
                             font=FONT_BOTON, relief="flat", command=self._mostrar_dashboard)
        btn_back.pack(fill='x', padx=30, pady=5, ipady=5)

    def _guardar_configuracion(self):
        try:
            # Validar y convertir
            nuevo_parado = float(self.entry_conf_parado.get().replace(',', '.'))
            nuevo_mov = float(self.entry_conf_mov.get().replace(',', '.'))

            if nuevo_parado < 0 or nuevo_mov < 0:
                raise ValueError("No se permiten valores negativos.")

            # Guardar
            self.config.set_tarifa("parado", nuevo_parado)
            self.config.set_tarifa("movimiento", nuevo_mov)
            
            logging.info(f"⚙️ Configuración actualizada: Parado={nuevo_parado}, Mov={nuevo_mov}")
            messagebox.showinfo("Éxito", "Tarifas actualizadas correctamente.")
            self._mostrar_dashboard()

        except ValueError:
            messagebox.showerror("Error", "Por favor, introduce valores numéricos válidos (ej: 0.05).")

    # ==========================================
    # LÓGICA DE NEGOCIO GUI (IGUAL QUE ANTES)
    # ==========================================
    def _gestion_ciclo_vida(self):
        if not self.taxi.en_trayecto:
            logging.info("UI: Botón INICIAR pulsado.")
            self.taxi.iniciar_trayecto()
            # UI Changes
            self.btn_principal.config(text=TXT_BTN_PARAR, bg=COLOR_SECUNDARIO)
            self.btn_marcha.config(state="normal", text="▶ PONER EN MARCHA", bg=COLOR_PRIMARIO)
            self.var_estado_txt.set("PARADO (Esperando)")
            self.lbl_estado.config(fg="#e67e22")
            # Bloquear botón config (se hace solo porque la vista cambia, pero por seguridad visual)
        else:
            logging.info("UI: Botón FINALIZAR pulsado.")
            if messagebox.askyesno("Finalizar", "¿Seguro que desea finalizar la carrera y cobrar?"):
                self._finalizar_y_mostrar_factura()

    def _alternar_marcha(self):
        logging.info("UI: Botón CAMBIO MARCHA pulsado.")
        nuevo_estado = self.taxi.alternar_estado_movimiento()
        
        if nuevo_estado == Estado.MOVIMIENTO:
            self.btn_marcha.config(text="⏸ DETENERSE", bg="#e67e22")
            self.var_estado_txt.set("🟢 EN MOVIMIENTO")
            self.lbl_estado.config(fg=COLOR_PRIMARIO)
        else:
            self.btn_marcha.config(text="▶ REANUDAR MARCHA", bg=COLOR_PRIMARIO)
            self.var_estado_txt.set("🟠 PARADO")
            self.lbl_estado.config(fg="#e67e22")

    def _finalizar_y_mostrar_factura(self):
        trayecto = self.taxi.finalizar_trayecto()
        
        # Reset UI
        self.btn_principal.config(text=TXT_BTN_INICIAR, bg=COLOR_PRIMARIO)
        self.btn_marcha.config(state="disabled", text="⏯ ARRANCAR / FRENAR", bg=COLOR_ACENTO)
        self.var_estado_txt.set("LIBRE")
        self.lbl_estado.config(fg=COLOR_TEXTO_MAIN)
        self.var_precio.set("LIBRE")
        self.var_tiempo.set("--:--")
        
        moneda = self.config.moneda
        factura = (
            f"📄 TICKET FINAL\n"
            f"--------------------------------\n"
            f"⏱ Tiempo Total: {trayecto.total_tiempo:.0f} seg\n"
            f"💰 Coste Total : {trayecto.total_coste:.2f} {moneda}\n"
            f"--------------------------------\n"
            f"DETALLE:\n"
            f"🚗 En Marcha: {trayecto.tiempo_movimiento:.0f}s -> {trayecto.coste_movimiento:.2f} {moneda}\n"
            f"🛑 Parado   : {trayecto.tiempo_parado:.0f}s -> {trayecto.coste_parado:.2f} {moneda}"
        )
        messagebox.showinfo("Factura", factura)

    def _loop_actualizar_ui(self):
        if self.taxi.en_trayecto and self.root.winfo_exists():
            tiempo, precio = self.taxi.obtener_info_tiempo_real()
            m, s = divmod(int(tiempo), 60)
            self.var_tiempo.set(f"{m:02d}:{s:02d}")
            self.var_precio.set(f"{precio:.2f} {self.config.moneda}")
            
        self.root.after(250, self._loop_actualizar_ui)

    def _accion_logout(self):
        if self.taxi.en_trayecto:
            messagebox.showwarning("Aviso", "Finalice la carrera antes de salir.")
            return
        logging.info(f"👋 Logout usuario: {self.auth.usuario_actual}")
        self.auth.logout()
        self._mostrar_login()