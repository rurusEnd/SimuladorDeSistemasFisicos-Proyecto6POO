import os
import time

# ==============================================================================
# 1. SIMULADORES DE EJEMPLO (Aquí importarás las clases de tus compañeros)
# Ejemplo futuro: from cinematica import MovimientoRectilineo
# ==============================================================================
class SimulacionMRU:
    """Molde de ejemplo: Movimiento Rectilíneo Uniforme"""
    def __init__(self, velocidad, tiempo):
        self.velocidad = velocidad
        self.tiempo = tiempo

    def calcular_distancia(self):
        return self.velocidad * self.tiempo

    def ejecutar(self):
        distancia = self.calcular_distancia()
        print(f"\n[RESULTADO MRU]")
        print(f"• Velocidad constante : {self.velocidad} m/s")
        print(f"• Tiempo transcurrido : {self.tiempo} s")
        print(f"• Distancia recorrida : {distancia:.2f} metros")


class SimulacionCaidaLibre:
    """Molde de ejemplo: Caída Libre"""
    def __init__(self, altura_inicial, gravedad=9.81):
        self.altura_inicial = altura_inicial
        self.gravedad = gravedad

    def calcular_tiempo_impacto(self):
        return ((2 * self.altura_inicial) / self.gravedad) ** 0.5

    def ejecutar(self):
        tiempo = self.calcular_tiempo_impacto()
        velocidad_final = self.gravedad * tiempo
        print(f"\n[RESULTADO CAÍDA LIBRE]")
        print(f"• Altura inicial      : {self.altura_inicial} m")
        print(f"• Gravedad aplicada   : {self.gravedad} m/s²")
        print(f"• Tiempo de caída     : {tiempo:.2f} s")
        print(f"• Velocidad de impacto: {velocidad_final:.2f} m/s")


# ==============================================================================
# 2. TU PARTE: PERSONA 6 - INTERFAZ DE CONSOLA Y MENÚ INTERACTIVO
# ==============================================================================
class MenuSimulador:
    def __init__(self):
        # Atributos del menú
        self.ejecutando = True
        self.historial = []  # Relación: El menú guarda los objetos simulados

    # --- MÉTODOS AUXILIARES (Limpieza y validación) ---
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pausar(self):
        input("\nPresiona [ENTER] para volver al menú principal...")

    def pedir_numero(self, mensaje, permitir_negativos=False):
        """Evita que el programa colapse si el usuario escribe letras o valores inválidos."""
        while True:
            try:
                valor = float(input(mensaje))
                if not permitir_negativos and valor < 0:
                    print("⚠️ Error: Este parámetro físico no puede ser negativo. Intenta de nuevo.")
                    continue
                return valor
            except ValueError:
                print("⚠️ Error: Debes ingresar un número válido (ej. 10 o 4.5).")

    # --- MÉTODOS DE INTERFAZ ---
    def mostrar_banner(self):
        print("=" * 55)
        print("        🔬 SIMULADOR FÍSICO INTERACTIVO v1.0 🔬")
        print("=" * 55)

    def mostrar_opciones(self):
        print("\nSelecciona el fenómeno físico a simular:")
        print("  [1] Movimiento Rectilíneo Uniforme (MRU)")
        print("  [2] Caída Libre")
        print("  [3] Ver historial de simulaciones")
        print("  [0] Salir del programa")
        print("-" * 55)

    # --- MÉTODOS DE CONEXIÓN CON LAS CLASES DE TUS COMPAÑEROS ---
    def gestionar_mru(self):
        print("\n--- CONFIGURACIÓN: MRU ---")
        v = self.pedir_numero("Ingresa la velocidad (m/s): ", permitir_negativos=True)
        t = self.pedir_numero("Ingresa el tiempo (s): ", permitir_negativos=False)

        # Instanciamos el objeto de la simulación y lo ejecutamos
        sim = SimulacionMRU(v, t)
        sim.ejecutar()
        self.historial.append(f"MRU (v={v} m/s, t={t} s)")

    def gestionar_caida_libre(self):
        print("\n--- CONFIGURACIÓN: CAÍDA LIBRE ---")
        h = self.pedir_numero("Ingresa la altura inicial (m): ", permitir_negativos=False)
        
        usar_g_defecto = input("¿Usar gravedad de la Tierra (9.81 m/s²)? (s/n): ").strip().lower()
        if usar_g_defecto == 'n':
            g = self.pedir_numero("Ingresa la gravedad personalizada (m/s²): ", permitir_negativos=False)
            sim = SimulacionCaidaLibre(h, g)
        else:
            sim = SimulacionCaidaLibre(h)

        sim.ejecutar()
        self.historial.append(f"Caída Libre (h={h} m)")

    def mostrar_historial(self):
        print("\n--- HISTORIAL DE SIMULACIONES EN ESTA SESIÓN ---")
        if not self.historial:
            print("Aún no has ejecutado ninguna simulación.")
        else:
            for indice, registro in enumerate(self.historial, start=1):
                print(f"  {indice}. {registro}")

    # --- MÉTODO PRINCIPAL (Bucle de ejecución) ---
    def iniciar(self):
        while self.ejecutando:
            self.limpiar_pantalla()
            self.mostrar_banner()
            self.mostrar_opciones()

            opcion = input("👉 Elige una opción: ").strip()

            if opcion == "1":
                self.gestionar_mru()
                self.pausar()
            elif opcion == "2":
                self.gestionar_caida_libre()
                self.pausar()
            elif opcion == "3":
                self.mostrar_historial()
                self.pausar()
            elif opcion == "0":
                print("\nCerrando el simulador... ¡Hasta luego! 👋")
                time.sleep(1)
                self.ejecutando = False
            else:
                print("\n❌ Opción no válida. Por favor elige entre 0 y 3.")
                time.sleep(1.5)


# ==============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==============================================================================
if __name__ == "__main__":
    app = MenuSimulador()
    app.iniciar()