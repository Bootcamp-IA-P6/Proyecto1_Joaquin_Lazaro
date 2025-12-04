import sys
import logging
from src.constantes import ARCHIVO_LOG
from src.configuracion import GestorConfiguracion
from src.gestor_historial import GestorHistorial
from src.autenticacion import GestorAuth
from src.modelo import Taximetro, Estado
from src.vista import VistaTerminal

# --- CONFIGURACIÓN DE LOGGING ---
logging.basicConfig(
    filename=ARCHIVO_LOG,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ControladorPrincipal:
    def __init__(self):
        # Modelo y Servicios
        self.conf = GestorConfiguracion()
        self.hist = GestorHistorial()
        self.auth = GestorAuth()
        self.taxi = Taximetro(self.conf, self.hist)
        
        # Vista (Inyección)
        self.vista = VistaTerminal()

    def flujo_login(self):
        intentos = 3
        while intentos > 0:
            user, password = self.vista.mostrar_login(intentos)
            
            if self.auth.login(user, password):
                self.vista.mostrar_login_exito(user)
                return True
            
            self.vista.mostrar_login_fallo()
            intentos -= 1
        
        self.vista.mostrar_bloqueo()
        logging.warning("Bloqueo de seguridad: Max intentos login alcanzados.")
        return False

    def flujo_configuracion(self):
        moneda = self.conf.moneda
        p_actual = self.conf.get_tarifa("parado")
        m_actual = self.conf.get_tarifa("movimiento")

        self.vista.mostrar_mensaje("\n⚙️  CONFIGURACIÓN (Escribe 'c' para cancelar)")
        
        # Pedir datos a través de la vista
        nuevo_p = self.vista.pedir_nueva_tarifa("Parado", p_actual, moneda)
        if nuevo_p is None: return

        nuevo_m = self.vista.pedir_nueva_tarifa("Movimiento", m_actual, moneda)
        if nuevo_m is None: return

        # Confirmación
        diff = f"Cambios: P({p_actual}->{nuevo_p}), M({m_actual}->{nuevo_m})"
        self.vista.mostrar_mensaje(f"🔍 {diff}")
        
        if self.vista.confirmar_accion("¿Guardar cambios?"):
            self.conf.set_tarifa("parado", nuevo_p)
            self.conf.set_tarifa("movimiento", nuevo_m)
            self.vista.mostrar_mensaje("✅ Configuración guardada.")
            logging.info(f"Configuración actualizada: {diff}")
        else:
            self.vista.mostrar_mensaje("🚫 Operación cancelada.")

    def flujo_carrera(self):
        trayecto = self.taxi.iniciar_carrera()
        moneda = self.conf.moneda
        logging.info("Trayecto iniciado.")
        self.vista.mostrar_mensaje("🏁 TRAYECTO INICIADO")

        while trayecto.estado_actual != Estado.FINALIZADO:
            # Mostrar estado actual (sin cálculos, eso lo hace el modelo si se pide)
            self.vista.mostrar_estado_carrera(
                trayecto.estado_actual, 
                0, 0, moneda # En loop estático mostramos 0, al cambiar mostramos real
            )
            
            comando = self.vista.obtener_comando_carrera(trayecto.estado_actual)

            try:
                coste, tiempo = 0, 0
                if comando == 'm':
                    coste, tiempo = self.taxi.cambiar_estado("movimiento")
                    self.vista.mostrar_mensaje("🚗 ¡EN MARCHA!")
                    logging.info("Estado: Movimiento")
                elif comando == 'p':
                    coste, tiempo = self.taxi.cambiar_estado("parado")
                    self.vista.mostrar_mensaje("🛑 ¡TAXI DETENIDO!")
                    logging.info("Estado: Parado")
                elif comando == 'f':
                    resumen = self.taxi.finalizar_carrera()
                    self.vista.mostrar_factura(resumen, moneda)
                    logging.info(f"Fin trayecto. Total: {resumen.total_coste}") # type: ignore
                    return
                else:
                    self.vista.mostrar_mensaje("❌ Comando desconocido.")
                    continue
                
                # Feedback del tramo recién terminado
                self.vista.mostrar_estado_carrera(trayecto.estado_actual, coste, tiempo, moneda)

            except ValueError as e:
                self.vista.mostrar_mensaje(f"⚠️ {e}")

    def iniciar_app(self):
        logging.info("App iniciada.")
        
        if not self.flujo_login():
            sys.exit(1)

        while True:
            # Datos frescos para el encabezado
            self.vista.mostrar_encabezado(
                self.conf.get_tarifa("parado"),
                self.conf.get_tarifa("movimiento"),
                self.conf.moneda
            )
            
            opcion = self.vista.mostrar_menu_principal()
            
            if opcion == '1':
                self.flujo_carrera()
            elif opcion == '2':
                self.flujo_configuracion()
            elif opcion == '3':
                self.vista.mostrar_mensaje("👋 Hasta pronto.")
                logging.info("Salida usuario.")
                sys.exit()
            else:
                self.vista.mostrar_mensaje("❌ Opción inválida.")

if __name__ == "__main__":
    app = ControladorPrincipal()
    app.iniciar_app()