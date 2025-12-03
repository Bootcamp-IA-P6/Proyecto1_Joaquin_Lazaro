from src.logica import TARIFA_PARADO, TARIFA_MOVIMIENTO

##Función para dar la bienvenida el usuario
def mostrar_bienvenida():
    print("\n" + "┌" + "─"*40 + "┐")
    print("│ 🚕  SISTEMA DE TAXÍMETRO DIGITAL v1.0   │")
    print("└" + "─"*40 + "┘")
    print("Instrucciones:")
    print(f" • Tarifa Parado      : {TARIFA_PARADO:.2f}€/s")
    print(f" • Tarifa Movimiento  : {TARIFA_MOVIMIENTO:.2f}€/s")
    print("-" * 42 + "\n")

##Contructor del main donde se llama a la función "Mostrar bienvenida"
def main():
    mostrar_bienvenida()
    input("Presiona ENTER para salir...")

if __name__ == "__main__":
    main()