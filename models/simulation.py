from models.physical_system import PhysicalSystem

class Result:
    """Clase auxiliar para demostrar Composición."""
    def __init__(self, time: float, position: float, velocity: float):
        self.time = time
        self.position = position
        self.velocity = velocity

    def __str__(self):
        return f"[T={self.time}s] Pos: {self.position:.2f} m, Vel: {self.velocity:.2f} m/s"


class Simulation:
    def __init__(self, name: str):
        self.name = name
        self.systems = []  # Agregación: Lista de sistemas físicos
        self.history = {}  # Composición: Historial de resultados generados aquí

    def add_system(self, system: PhysicalSystem):
        self.systems.append(system)
        self.history[system.name] = []

    def run_all(self, time: float):
        """Ejecuta la simulación para todos los sistemas registrados."""
        for system in self.systems:
            pos = system.calculate_position(time)
            vel = system.calculate_velocity(time)
            
            # Composición: Se instancia el resultado dentro de la simulación
            new_result = Result(time, pos, vel)
            self.history[system.name].append(new_result)

    def show_summary(self):
        """Muestra los resultados guardados."""
        print(f"\n=== REPORTE DE SIMULACIÓN: {self.name} ===")
        for sys_name, results in self.history.items():
            print(f"\n-> Sistema: {sys_name}")
            for res in results:
                print(f"   {res}")