from models.free_fall import FreeFall
from models.linear_motion import LinearMotion

def run_simulation(system, time: float):
    # Función polimórfica: no importa si es MRUV o Caída Libre, 
    # el método se llama igual pero actúa distinto.
    print(f"\n--- Simulando: {system.name} ---")
    pos = system.calculate_position(time)
    vel = system.calculate_velocity(time)
    print(f"Tiempo: {time} s")
    print(f"Posición: {pos:.2f} m")
    print(f"Velocidad: {vel:.2f} m/s")

def main():
    print("=== SIMULADOR DE SISTEMAS FÍSICOS ===")
    
    # Instanciación de diferentes objetos (heredan de PhysicalSystem)
    caida = FreeFall(initial_height=50.0)
    mruv = LinearMotion(initial_position=0.0, initial_velocity=10.0, acceleration=2.5)

    tiempo_simulacion = 4.0 # segundos

    # Demostración polimórfica
    run_simulation(caida, tiempo_simulacion)
    run_simulation(mruv, tiempo_simulacion)

if __name__ == "__main__":
    main()