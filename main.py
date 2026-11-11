from models.free_fall import FreeFall
from models.linear_motion import LinearMotion
from models.simulation import Simulation

def main():
    print("=== INICIANDO SIMULADOR DE SISTEMAS FÍSICOS ===")
    
    # 1. Crear el gestor de la simulación
    sim = Simulation("Prueba de Laboratorio 1")
    
    # 2. Registrar entidades (Alcance mínimo)
    caida = FreeFall(initial_height=100.0)
    mruv = LinearMotion(initial_position=0.0, initial_velocity=5.0, acceleration=2.0)
    
    sim.add_system(caida)
    sim.add_system(mruv)
    
    # 3. Menú interactivo básico
    while True:
        try:
            entrada = input("\nIngrese el tiempo a simular en segundos (o 'q' para salir): ")
            if entrada.lower() == 'q':
                break
                
            tiempo = float(entrada)
            if tiempo < 0:
                print("Error: El tiempo no puede ser negativo.")
                continue
                
            # Ejecutar operaciones del dominio polimórficamente
            sim.run_all(tiempo)
            print(f"Simulación calculada para t = {tiempo}s exitosamente.")
            
        except ValueError:
            print("Error: Por favor ingrese un número válido.")
            
    # 4. Mostrar resultados guardados al finalizar
    sim.show_summary()

if __name__ == "__main__":
    main()