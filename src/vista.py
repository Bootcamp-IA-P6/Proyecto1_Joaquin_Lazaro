import sys
from getpass import getpass
from src.utils import leer_float_seguro
from src.modelo import Estado

class VistaTerminal:
    """Encargada de toda la entrada/salida por consola."""

    def mostrar_encabezado(self, tarifa_parado, tarifa_movimiento, moneda):
        print("\n" + "┌" + "─"*42 + "┐")
        print("│ 🚕  SISTEMA DE TAXÍMETRO DIGITAL v3.0    │")
        print("└" + "─"*42 + "┘")
        print(f" • Tarifa Parado      : {tarifa_parado:.2f}{moneda}/s")
        print(f" • Tarifa Movimiento  : {tarifa_movimiento:.2f}{moneda}/s")
        print("-" * 44 + "\n")

    def mostrar_menu_principal(self):
        print("\n🔵 MENÚ PRINCIPAL")
        print("1. 🚕 Iniciar nuevo trayecto")
        print("2. ⚙️  Configurar tarifas")
        print("3. 👋 Salir")
        return input("Selecciona una opción: ").strip()

    def mostrar_login(self, intentos_restantes):
        print(f"\n🔒 INICIO DE SESIÓN (Intentos: {intentos_restantes})")
        u = input(" 👤 Usuario: ").strip()
        p = getpass(" 🔑 Contraseña: ").strip()
        return u, p

    def mostrar_login_exito(self, usuario):
        print(f"\n✅ Bienvenido al sistema, {usuario}.")

    def mostrar_login_fallo(self):
        print("❌ Credenciales incorrectas.")

    def mostrar_bloqueo(self):
        print("\n🚫 ACCESO DENEGADO. Sistema bloqueado.")

    def mostrar_estado_carrera(self, estado: Estado, coste: float, tiempo: float, moneda: str):
        print(f"\n📢 Estado actual: {estado.value.upper()}")
        if coste > 0 or tiempo > 0:
            print(f"   ⏱️  Último tramo: {tiempo:.2f}s -> {coste:.2f}{moneda}")

    def obtener_comando_carrera(self, estado: Estado):
        opciones = "[p]arar, [f]inalizar" if estado == Estado.MOVIMIENTO else "[m]over, [f]inalizar"
        print(f"👉 Opciones: {opciones}")
        return input(" > ").strip().lower()

    def mostrar_mensaje(self, mensaje):
        print(mensaje)

    def mostrar_factura(self, resumen, moneda):
        print("\n" + "="*44)
        print("             📄 FACTURA FINAL             ")
        print("="*44)
        print(f" ⏱️  TIEMPO TOTAL       : {resumen.total_tiempo:.2f}s")
        print(f" 💰 COSTE TOTAL        : {resumen.total_coste:.2f}{moneda}")
        print("="*44)
        print(" DESGLOSE:")
        print(f"   - En Movimiento : {resumen.tiempo_movimiento:.2f}s ({resumen.coste_movimiento:.2f}{moneda})")
        print(f"   - Parado        : {resumen.tiempo_parado:.2f}s ({resumen.coste_parado:.2f}{moneda})")
        print("="*44 + "\n")

    def pedir_nueva_tarifa(self, nombre_tarifa, valor_actual, moneda):
        """Usa la utilidad robusta pero gestionada desde la vista."""
        msg = f" > Nuevo precio {nombre_tarifa} (Actual: {valor_actual}{moneda}/s): "
        return leer_float_seguro(msg)

    def confirmar_accion(self, mensaje):
        resp = input(f"\n💾 {mensaje} (s/n): ").strip().lower()
        return resp == 's'