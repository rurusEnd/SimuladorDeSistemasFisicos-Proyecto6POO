import os
import time

# ==============================================================================
# IMPORTACIÓN DE MÓDULOS DE TUS COMPAÑEROS
# (Si pruebas tu archivo solo antes de que ellos suban su código,
#  el bloque try-except evita que falle y usa simuladores de respaldo)
# ==============================================================================
try:
    from modelos.movimiento_rectilineo import MovimientoRectilineo
    from modelos.caida_libre import CaidaLibre
    from modelos.movimiento_parabolico import MovimientoParabolico
    from modelos.movimiento_circular import MovimientoCircular
    from modelos.oscilador import Oscilador
    from modelos.simulacion import Simulacion
    from servicios.validador import Validador
    MODULOS_COMPLETOS = True
except ImportError:
    MODULOS_COMPLETOS = False


# ==============================================================================
# CLASE DE LA INTERFAZ DE CONSOLA (TU PARTE - PERSONA 6)
# ==============================================================================
class MenuConsola:
    def __init__(self):
        self.ejecutando = True
        # Relación con Persona 4: El menú administra una instancia de Simulacion
        self.simulacion_actual = Simulacion("Sesión de Laboratorio") if MODULOS_COMPLETOS else None
        self.historial_local = []

    # --- UTILIDADES DE PANTALLA ---
    def limpiar_pantalla(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pausar(self):
        input("\nPresiona [ENTER] para continuar...")

    def leer_float(self, mensaje, permitir_negativos=True, permitir_cero=True):
        """
        Captura entradas numéricas del usuario. Si Persona 5 creó métodos
        en Validador, también captura los ValueError lanzados por sus @property.
        """
        while True:
            try:
                valor = float(input(mensaje))
                if not permitir_negativos and valor < 0:
                    print("⚠️  El valor no puede ser negativo.")
                    continue
                if not permitir_cero and valor == 0:
                    print("⚠️  El valor no puede ser cero.")
                    continue
                return valor
            except ValueError:
                print("⚠️  Entrada inválida. Ingresa un número real (ej. 12.5).")

    # --- DISEÑO VISUAL ---
    def mostrar_encabezado(self):
        print("=" * 62)
        print("        ⚛️  SIMULADOR DE SISTEMAS FÍSICOS (POO)  ⚛️")
        print("=" * 62)
        estado = "✅ Módulos conectados" if MODULOS_COMPLETOS else "⚠️ Modo interfaz independiente"
        print(f" Estado del sistema: {estado}")
        print("-" * 62)

    def mostrar_menu_principal(self):
        print("\nSeleccione el sistema físico que desea instanciar y simular:")
        print("  [1] Movimiento Rectilíneo (MRU / MRUV)      [Persona 2]")
        print("  [2] Caída Libre                            [Persona 2]")
        print("  [3] Movimiento Parabólico (Proyectiles)    [Persona 3]")
        print("  [4] Movimiento Circular                    [Persona 3]")
        print("  [5] Sistema Oscilatorio (Resorte/Péndulo)  [Persona 3]")
        print("-" * 62)
        print("  [6] Ejecutar simulación grupal (Polimorfismo) [Persona 4]")
        print("  [7] Ver resultados acumulados")
        print("  [0] Salir")
        print("=" * 62)

    # --- MÉTODOS DE CAPTURA DE PARÁMETROS POR SISTEMA ---
    def configurar_rectilineo(self):
        print("\n--- CONFIGURAR MOVIMIENTO RECTILÍNEO (MRU / MRUV) ---")
        x0 = self.leer_float("Posición inicial x0 (m): ")
        v0 = self.leer_float("Velocidad inicial v0 (m/s): ")
        a = self.leer_float("Aceleración a (m/s²) [0 para MRU]: ")
        t = self.leer_float("Tiempo de evaluación t (s): ", permitir_negativos=False)

        sistema = MovimientoRectilineo(x0, v0, a, t)
        self._procesar_sistema(sistema, f"Rectilíneo (x0={x0}, v0={v0}, a={a}, t={t})")

    def configurar_caida_libre(self):
        print("\n--- CONFIGURAR CAÍDA LIBRE ---")
        h = self.leer_float("Altura inicial h (m): ", permitir_negativos=False)
        v0 = self.leer_float("Velocidad inicial vertical v0 (m/s) [0 si se suelta]: ")
        t = self.leer_float("Tiempo t (s): ", permitir_negativos=False)

        sistema = CaidaLibre(h, v0, t)
        self._procesar_sistema(sistema, f"Caída Libre (h={h}m, v0={v0}m/s, t={t}s)")

    def configurar_parabolico(self):
        print("\n--- CONFIGURAR MOVIMIENTO PARABÓLICO ---")
        v0 = self.leer_float("Velocidad inicial de disparo v0 (m/s): ", permitir_negativos=False)
        angulo = self.leer_float("Ángulo de lanzamiento (grados 0-90): ", permitir_negativos=False)
        t = self.leer_float("Tiempo t (s): ", permitir_negativos=False)

        sistema = MovimientoParabolico(v0, angulo, t)
        self._procesar_sistema(sistema, f"Parabólico (v0={v0}m/s, θ={angulo}°, t={t}s)")

    def configurar_circular(self):
        print("\n--- CONFIGURAR MOVIMIENTO CIRCULAR ---")
        radio = self.leer_float("Radio de trayectoria r (m): ", permitir_negativos=False, permitir_cero=False)
        omega = self.leer_float("Velocidad angular ω (rad/s): ")
        t = self.leer_float("Tiempo t (s): ", permitir_negativos=False)

        sistema = MovimientoCircular(radio, omega, t)
        self._procesar_sistema(sistema, f"Circular (r={radio}m, ω={omega}rad/s, t={t}s)")

    def configurar_oscilador(self):
        print("\n--- CONFIGURAR SISTEMA OSCILATORIO ---")
        amplitud = self.leer_float("Amplitud A (m): ", permitir_negativos=False, permitir_cero=False)
        masa = self.leer_float("Masa m (kg): ", permitir_negativos=False, permitir_cero=False)
        constante_k = self.leer_float("Constante elástica k (N/m): ", permitir_negativos=False, permitir_cero=False)
        t = self.leer_float("Tiempo t (s): ", permitir_negativos=False)

        sistema = Oscilador(amplitud, masa, constante_k, t)
        self._procesar_sistema(sistema, f"Oscilador (A={amplitud}m, m={masa}kg, k={constante_k}N/m)")

    # --- EJECUCIÓN POLIMÓRFICA Y CONEXIÓN CON PERSONA 4 Y 5 ---
    def _procesar_sistema(self, sistema, resumen):
        """
        Aquí ocurre el polimorfismo: sin importar qué clase física sea,
        todas heredan de SistemaFisico (Persona 1) y responden a los mismos métodos.
        """
        print("\n" + "*" * 45)
        print("  📊 RESULTADOS DE LA SIMULACIÓN")
        print("*" * 45)
        
        # Llamada polimórfica al contrato definido por Persona 1
        resultado = sistema.simular()
        print(resultado)

        # Agregamos el objeto a la clase Simulacion de Persona 4
        if self.simulacion_actual is not None:
            self.simulacion_actual.agregar_sistema(sistema)
        
        self.historial_local.append((resumen, resultado))

    def ejecutar_simulacion_grupal(self):
        """Demuestra polimorfismo ejecutando todos los sistemas agregados en Simulacion."""
        print("\n--- EJECUCIÓN POR LOTES (POLIMORFISMO) ---")
        if self.simulacion_actual is not None:
            self.simulacion_actual.ejecutar_todo()
        else:
            print("Aún no se ha conectado el módulo 'modelos/simulacion.py' de Persona 4.")

    def ver_historial(self):
        print("\n--- HISTORIAL DE RESULTADOS DE LA SESIÓN ---")
        if not self.historial_local:
            print("No hay simulaciones registradas todavía.")
            return
        for i, (desc, res) in enumerate(self.historial_local, start=1):
            print(f"\n[{i}] {desc}")
            print(f"    -> {res}")

    # --- BUCLE PRINCIPAL ---
    def iniciar(self):
        while self.ejecutando:
            self.limpiar_pantalla()
            self.mostrar_encabezado()
            self.mostrar_menu_principal()

            opcion = input("👉 Elige una opción [0-7]: ").strip()

            # Este try-except atrapa cualquier error de validación (@property)
            # que lancen las clases de Persona 2, 3 o 5 al instanciarse.
            try:
                if opcion == "1":
                    self.configurar_rectilineo()
                    self.pausar()
                elif opcion == "2":
                    self.configurar_caida_libre()
                    self.pausar()
                elif opcion == "3":
                    self.configurar_parabolico()
                    self.pausar()
                elif opcion == "4":
                    self.configurar_circular()
                    self.pausar()
                elif opcion == "5":
                    self.configurar_oscilador()
                    self.pausar()
                elif opcion == "6":
                    self.ejecutar_simulacion_grupal()
                    self.pausar()
                elif opcion == "7":
                    self.ver_historial()
                    self.pausar()
                elif opcion == "0":
                    print("\nFinalizando simulador físico... ¡Éxitos en la sustentación!")
                    time.sleep(1)
                    self.ejecutando = False
                else:
                    print("\n❌ Opción incorrecta. Elige un número del 0 al 7.")
                    time.sleep(1.2)

            except ValueError as error_validacion:
                # Captura los raise ValueError de los setters (@property) de Persona 5
                print(f"\n🛑 ERROR DE VALIDACIÓN FÍSICA: {error_validacion}")
                self.pausar()
            except Exception as error_inesperado:
                print(f"\n⚠️ Ocurrió un problema inesperado: {error_inesperado}")
                self.pausar()


if __name__ == "__main__":
    app = MenuConsola()
    app.iniciar()