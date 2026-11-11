from math import isfinite

from models.circular_motion import CircularMotion
from models.free_fall import FreeFall
from models.linear_motion import LinearMotion
from models.oscillator import Oscillator
from models.projectile import ProjectileMotion
from models.physical_system import PhysicalSystem
from models.simulation import Simulation


def read_float(
    prompt: str,
    minimum: float | None = None,
    *,
    strictly_greater: bool = False,
    default: float | None = None,
) -> float:
    while True:
        raw_value = input(prompt).strip()
        if not raw_value and default is not None:
            return default
        try:
            value = float(raw_value)
        except ValueError:
            print("Ingrese un número válido.")
            continue

        valid = isfinite(value)
        if minimum is not None:
            valid = valid and (
                value > minimum if strictly_greater else value >= minimum
            )
        if valid:
            return value

        if minimum is None:
            print("El valor debe ser un número finito.")
        else:
            relation = "mayor que" if strictly_greater else "mayor o igual que"
            print(f"El valor debe ser {relation} {minimum}.")


def create_system() -> PhysicalSystem:
    print(
        "\nTipos de sistema:"
        "\n1. Movimiento rectilíneo (MRUV)"
        "\n2. Caída libre"
        "\n3. Movimiento parabólico"
        "\n4. Movimiento circular"
        "\n5. Oscilador armónico"
    )
    while True:
        choice = input("Seleccione el tipo: ").strip()
        if choice in {"1", "2", "3", "4", "5"}:
            break
        print("Seleccione una opción del 1 al 5.")

    if choice == "1":
        system = LinearMotion(
            read_float("Posición inicial (m): "),
            read_float("Velocidad inicial (m/s): "),
            read_float("Aceleración (m/s²): "),
        )
    elif choice == "2":
        system = FreeFall(
            read_float("Altura inicial (m): ", 0),
            read_float("Gravedad (m/s²) [9.81]: ", default=9.81),
        )
    elif choice == "3":
        system = ProjectileMotion(
            read_float("Altura inicial (m): ", 0),
            read_float("Rapidez inicial (m/s): ", 0),
            read_float("Ángulo respecto a la horizontal (grados): "),
            read_float("Gravedad (m/s²) [9.81]: ", default=9.81),
        )
    elif choice == "4":
        system = CircularMotion(
            read_float("Radio (m): ", 0),
            read_float("Velocidad angular (rad/s): "),
            read_float("Ángulo inicial (grados) [0]: ", default=0),
        )
    else:
        system = Oscillator(
            read_float("Amplitud (m): ", 0),
            read_float("Frecuencia angular (rad/s): ", 0, strictly_greater=True),
            read_float("Fase inicial (grados) [0]: ", default=0),
        )

    name = input(f"Nombre del sistema [{system.name}]: ").strip()
    if name:
        system.name = name
    return system


def main() -> None:
    simulation = Simulation("Simulador de sistemas físicos")
    simulation.add_system(FreeFall(initial_height=100.0))
    simulation.add_system(
        LinearMotion(initial_position=0.0, initial_velocity=5.0, acceleration=2.0)
    )

    print("=== SIMULADOR DE SISTEMAS FÍSICOS ===")
    while True:
        print(
            "\n1. Agregar sistema"
            "\n2. Ejecutar simulación"
            "\n3. Comparar resultados"
            "\n4. Guardar resultados en CSV"
            "\n5. Salir"
        )
        choice = input("Opción: ").strip()

        if choice == "1":
            system = create_system()
            name = simulation.add_system(system)
            print(f"Sistema '{name}' agregado.")
        elif choice == "2":
            duration = read_float("Duración total (s): ", 0)
            time_step = read_float(
                "Intervalo entre muestras (s): ", 0, strictly_greater=True
            )
            try:
                count = simulation.simulate(duration, time_step)
            except (ValueError, ArithmeticError) as error:
                print(f"No se pudo ejecutar la simulación: {error}")
                continue
            print(f"Simulación completada: {count} instantes calculados.")
            simulation.show_comparison()
        elif choice == "3":
            simulation.show_comparison()
        elif choice == "4":
            file_path = input("Archivo CSV [resultados.csv]: ").strip()
            try:
                saved_path = simulation.save_csv(file_path or "resultados.csv")
            except (OSError, ValueError) as error:
                print(f"No se pudieron guardar los resultados: {error}")
                continue
            print(f"Resultados guardados en: {saved_path.resolve()}")
        elif choice == "5":
            print("Simulador finalizado.")
            break
        else:
            print("Opción inválida. Elija una opción del 1 al 5.")


if __name__ == "__main__":
    main()
